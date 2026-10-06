package com.eduai4.app.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.eduai4.app.data.ProgressDto
import com.eduai4.app.viewmodel.MainViewModel

private data class Badge(val icon: String, val name: String, val earned: (ProgressDto) -> Boolean)

private val badges = listOf(
    Badge("🏆", "Hoàn thành 1 bài") { it.quizzes_done >= 1 },
    Badge("⭐", "Đạt 100%") { it.perfect_quizzes >= 1 },
    Badge("🔥", "Học 3 ngày liên tiếp") { it.streak >= 3 },
    Badge("📚", "Hoàn thành 5 bài") { it.quizzes_done >= 5 },
)

@Composable
fun ProgressScreen(main: MainViewModel, onTopic: (Int) -> Unit, onLogout: () -> Unit) {
    val state by main.progress.collectAsState()
    LaunchedEffect(Unit) { main.load() }

    StateView(state, onRetry = { main.load() }) { p ->
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)) {
            Text("Tiến độ của em", fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(12.dp))
            AppCard {
                p.subjects.forEach { s ->
                    Text("${s.subject}: ${s.accuracy?.let { "$it%" } ?: "chưa làm"}", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    LinearProgressIndicator(
                        progress = { (s.accuracy ?: 0) / 100f },
                        modifier = Modifier.fillMaxWidth().height(12.dp).padding(bottom = 0.dp),
                    )
                    Spacer(Modifier.height(10.dp))
                }
            }
            Spacer(Modifier.height(16.dp))
            Text("Cần ôn thêm", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(8.dp))
            if (p.weak_topics.isEmpty()) {
                AppCard { Text("Chưa có chủ đề nào yếu. Cứ tiếp tục nhé! 💪", fontSize = 18.sp) }
            } else p.weak_topics.forEach { t ->
                AppCard(Modifier.padding(bottom = 10.dp).clickable { onTopic(t.topic_id) }) {
                    Text("⚠️ ${t.topic} (${t.subject})", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Đúng ${t.accuracy}% – bấm để luyện lại", fontSize = 16.sp)
                }
            }
            Spacer(Modifier.height(16.dp))
            Text("Huy hiệu", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(8.dp))
            AppCard {
                badges.forEach { b ->
                    Text("${b.icon} ${b.name}", fontSize = 18.sp, modifier = Modifier.alpha(if (b.earned(p)) 1f else 0.35f).padding(vertical = 4.dp))
                }
            }
            Spacer(Modifier.height(16.dp))
            BigButton("Đăng xuất", onLogout, container = Color.White, content = Ink)
        }
    }
}
