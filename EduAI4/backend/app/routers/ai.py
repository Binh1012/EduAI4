"""AI tutor. The API key lives only on the server; the Android app never sees it."""
import time
from collections import defaultdict, deque

import httpx
from fastapi import APIRouter, Depends, HTTPException

from ..config import settings
from ..deps import current_user
from ..models import User
from ..schemas import TutorIn, TutorOut

router = APIRouter(tags=["ai"])

SYSTEM_PROMPT = (
    "Bạn là cô giáo trợ giảng thân thiện cho học sinh lớp 4 ở Việt Nam. "
    "Luôn trả lời bằng tiếng Việt đơn giản, tối đa 5 câu ngắn. "
    "Giải thích từng bước, dùng ví dụ gần gũi (chia bánh, chia kẹo...). "
    "Khuyến khích em tự suy nghĩ: có thể đặt một câu hỏi gợi mở thay vì chỉ đưa đáp án. "
    "Chỉ trả lời về học tập (Toán, Tiếng Việt, Khoa học, Lịch sử - Địa lý, Tiếng Anh). "
    "Không hỏi hoặc lưu thông tin cá nhân. Nếu câu hỏi không phù hợp với trẻ em hoặc ngoài học tập, "
    "hãy nhẹ nhàng từ chối và mời em hỏi một bài học."
)
FALLBACK = "Cô chưa trả lời được lúc này. Em thử đọc lại phần giải thích của câu hỏi nhé, rồi hỏi cô lại sau."

_calls = defaultdict(deque)  # user_id -> timestamps (simple in-memory rate limit)


def _check_rate(user_id: int):
    q, now = _calls[user_id], time.time()
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= settings.AI_RATE_LIMIT:
        raise HTTPException(429, "Em hỏi nhiều quá rồi, nghỉ một chút rồi hỏi tiếp nhé!")
    q.append(now)


@router.post("/ai/tutor", response_model=TutorOut)
def tutor(body: TutorIn, user: User = Depends(current_user)):
    _check_rate(user.id)
    if not settings.ANTHROPIC_API_KEY:
        return TutorOut(answer="Chưa bật trợ giảng AI. Hãy nhờ thầy cô cấu hình ANTHROPIC_API_KEY cho máy chủ nhé.")
    try:
        r = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": settings.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01"},
            json={"model": settings.AI_MODEL, "max_tokens": 400, "system": SYSTEM_PROMPT,
                  "messages": [{"role": "user", "content": body.question.strip()}]},
            timeout=30,
        )
        r.raise_for_status()
        text = "".join(b.get("text", "") for b in r.json().get("content", []) if b.get("type") == "text")
        return TutorOut(answer=text.strip() or FALLBACK)
    except httpx.HTTPError:
        return TutorOut(answer=FALLBACK)
