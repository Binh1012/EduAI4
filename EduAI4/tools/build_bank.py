"""Builds the offline question bank (JSON) used by the app. Run: python tools/build_bank.py"""
import json, random
from math import gcd
R = random.Random(2024)
COL = {"Toán": ("📐", "#2f7bff"), "Tiếng Việt": ("📖", "#ff7a45"), "Khoa học": ("🔬", "#2eb872"),
       "Lịch sử – Địa lý": ("🗺️", "#9b5de5"), "Tiếng Anh": ("🔤", "#ff4f9a")}

def mk(text, correct, wrongs, exp, d=1):
    ws = [w for w in dict.fromkeys(map(str, wrongs)) if w != str(correct)]
    opts = [str(correct)] + ws[:3]
    R.shuffle(opts)
    return dict(text=text, options=opts, correct_index=opts.index(str(correct)), explanation=exp, difficulty=d)

def tf(text, val, exp):
    return dict(text=text, options=["Đúng", "Sai"], correct_index=0 if val else 1, explanation=exp, difficulty=1)

def nw(c, extra=()):
    c0 = [c + 10, c - 10, c + 100, c - 100, c + 1, c - 1, c + 2, c - 2] if c > 20 else [c + 1, c - 1, c + 2, c - 2, c + 3, c + 5]
    pool = [x for x in list(extra) + R.sample(c0, len(c0)) if x != c and x > 0]
    return list(dict.fromkeys(pool))[:3]

def fmt(n): return f"{n:,}".replace(",", ".")
def lvl(n): return 1 if n < 1000 else 2 if n < 6000 else 3

# ---------- TOÁN (sinh tự động) ----------
def gen_add(n=20):
    out = []
    for _ in range(n):
        a, b = R.randint(100, 9999), R.randint(100, 9999); c = a + b
        out.append(mk(f"{fmt(a)} + {fmt(b)} = ?", fmt(c), [fmt(x) for x in nw(c, [c + 10, c - 100, c + 1000])],
                      f"{fmt(a)} + {fmt(b)} = {fmt(c)}. Cộng từ hàng đơn vị, nhớ sang hàng tiếp theo.", lvl(c)))
    return out

def gen_sub(n=20):
    out = []
    for _ in range(n):
        a = R.randint(500, 9999); b = R.randint(100, a - 50); c = a - b
        out.append(mk(f"{fmt(a)} − {fmt(b)} = ?", fmt(c), [fmt(x) for x in nw(c, [c + 10, c - 100, c + 1000])],
                      f"{fmt(a)} − {fmt(b)} = {fmt(c)}. Thử lại: {fmt(c)} + {fmt(b)} = {fmt(a)}.", lvl(a)))
    return out

def gen_mul(n=20):
    out = []
    for _ in range(n):
        a, b = R.randint(12, 999), R.randint(2, 20); c = a * b
        out.append(mk(f"{fmt(a)} × {b} = ?", fmt(c), [fmt(x) for x in nw(c, [a * (b + 1), a * (b - 1), c + 10])],
                      f"{fmt(a)} × {b} = {fmt(c)}.", 1 if c < 1000 else 2 if c < 5000 else 3))
    return out

def gen_div(n=20):
    out = []
    for _ in range(n):
        b, q = R.randint(2, 9), R.randint(11, 150); a = b * q
        out.append(mk(f"{fmt(a)} : {b} = ?", fmt(q), [fmt(x) for x in nw(q, [q + 10, q - 10, q + 1])],
                      f"Vì {b} × {q} = {fmt(a)} nên {fmt(a)} : {b} = {q}.", 1 if q < 40 else 2 if q < 100 else 3))
    return out

def gen_compare(n=15):
    out = []
    for i in range(10):
        nums = R.sample(range(1000, 99999), 4); big = (i % 2 == 0)
        c = max(nums) if big else min(nums)
        out.append(mk(f"Số nào {'lớn' if big else 'bé'} nhất trong các số sau?", fmt(c), [fmt(x) for x in nums if x != c],
                      "So sánh từ hàng cao nhất (bên trái): số có nhiều chữ số hơn thì lớn hơn, bằng chữ số thì so từng hàng.", 2))
    for _ in range(5):
        a = R.randint(1000, 9999); b = a + R.choice([-1, 1]) * R.randint(1, 800); sg = ">" if a > b else "<"
        out.append(mk(f"Điền dấu thích hợp: {fmt(a)} … {fmt(b)}", sg, [">" if sg == "<" else "<", "=", "không so sánh được"],
                      f"{fmt(a)} {sg} {fmt(b)}.", 1))
    return out

def gen_frac():
    out = [tf("1/2 lớn hơn 1/3.", True, "Chia chiếc bánh thành 2 phần thì mỗi phần to hơn khi chia thành 3 phần."),
           mk("Phân số nào lớn nhất?", "1/2", ["1/4", "1/3", "1/5"], "Tử số bằng nhau thì mẫu số càng bé, phân số càng lớn.", 1),
           mk("3/4 của 20 là bao nhiêu?", 15, [10, 12, 16], "20 : 4 = 5, rồi 5 × 3 = 15.", 2),
           tf("Phân số 4/4 bằng 1.", True, "Tử số bằng mẫu số thì phân số bằng 1."),
           mk("Phân số nào bé hơn 1?", "3/5", ["5/5", "7/5", "9/5"], "Phân số bé hơn 1 có tử số bé hơn mẫu số.", 1)]
    for _ in range(7):
        n = R.randint(5, 12); a = R.randint(1, n - 2); b = R.randint(1, n - a - 1) if n - a - 1 >= 1 else 1; c = a + b
        out.append(mk(f"{a}/{n} + {b}/{n} = ?", f"{c}/{n}", [f"{c}/{2*n}", f"{abs(a-b)}/{n}", f"{c}/{n+1}"],
                      f"Mẫu số giống nhau: cộng các tử số, giữ nguyên mẫu số. {a} + {b} = {c}.", 2))
    for _ in range(6):
        n = R.randint(6, 13); a = R.randint(3, n - 1); b = R.randint(1, a - 1); c = a - b
        out.append(mk(f"{a}/{n} − {b}/{n} = ?", f"{c}/{n}", [f"{c}/{2*n}", f"{a+b}/{n}", f"{c}/{n-1}"],
                      f"Trừ các tử số, giữ nguyên mẫu số. {a} − {b} = {c}.", 2))
    for _ in range(4):
        p, q = R.choice([(1, 2), (1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (5, 6), (3, 8)]); k = R.choice([2, 3, 4, 5])
        out.append(mk(f"Rút gọn phân số {p*k}/{q*k}", f"{p}/{q}", [f"{p}/{q+1}", f"{p+1}/{q}", f"{p*k}/{q*k-1}"],
                      f"Chia cả tử số và mẫu số cho {k}: {p*k}/{q*k} = {p}/{q}.", 3))
    for _ in range(3):
        p, q = R.choice([(1, 2), (1, 3), (2, 3), (3, 4), (2, 5)]); k = R.choice([2, 3, 4])
        out.append(mk(f"Phân số nào bằng {p}/{q}?", f"{p*k}/{q*k}", [f"{p*k}/{q*k+1}", f"{p+k}/{q+k}", f"{p*k}/{q+k}"],
                      f"Nhân cả tử số và mẫu số với {k}: {p}/{q} = {p*k}/{q*k}.", 2))
    return out

def gen_geo():
    out = [mk("Góc vuông có số đo bằng bao nhiêu độ?", "90 độ", ["45 độ", "60 độ", "180 độ"], "Góc vuông bằng 90 độ, như góc của quyển vở.", 1),
           tf("Hình vuông có 4 cạnh bằng nhau.", True, "Hình vuông có 4 cạnh bằng nhau và 4 góc vuông."),
           tf("Hình chữ nhật có 4 cạnh bằng nhau.", False, "Hình chữ nhật chỉ có các cạnh đối bằng nhau."),
           mk("Hình bình hành có các cặp cạnh đối như thế nào?", "song song và bằng nhau", ["vuông góc với nhau", "không bằng nhau", "cắt nhau"],
              "Hình bình hành có hai cặp cạnh đối song song và bằng nhau.", 2)]
    for _ in range(7):
        a, b = R.randint(5, 40), R.randint(3, 30); p = (a + b) * 2
        out.append(mk(f"Hình chữ nhật dài {a} cm, rộng {b} cm. Chu vi là bao nhiêu?", f"{p} cm", [f"{a+b} cm", f"{a*b} cm", f"{p+a} cm"],
                      f"Chu vi = (dài + rộng) × 2 = ({a} + {b}) × 2 = {p} cm.", 2))
    for _ in range(7):
        a, b = R.randint(4, 25), R.randint(3, 20); s = a * b
        out.append(mk(f"Hình chữ nhật dài {a} cm, rộng {b} cm. Diện tích là bao nhiêu?", f"{s} cm²", [f"{(a+b)*2} cm²", f"{s+a} cm²", f"{a+b} cm²"],
                      f"Diện tích = dài × rộng = {a} × {b} = {s} cm².", 2))
    for i in range(6):
        a = R.randint(3, 30)
        if i % 2 == 0:
            out.append(mk(f"Hình vuông có cạnh {a} cm. Chu vi là bao nhiêu?", f"{4*a} cm", [f"{2*a} cm", f"{a*a} cm", f"{4*a+4} cm"], f"Chu vi hình vuông = cạnh × 4 = {a} × 4 = {4*a} cm.", 1))
        else:
            out.append(mk(f"Hình vuông có cạnh {a} cm. Diện tích là bao nhiêu?", f"{a*a} cm²", [f"{4*a} cm²", f"{2*a} cm²", f"{a*a+a} cm²"], f"Diện tích hình vuông = cạnh × cạnh = {a} × {a} = {a*a} cm².", 2))
    return out

def gen_word():
    out = []
    for _ in range(3):
        a, b = R.randint(20, 300), R.randint(10, 200)
        out.append(mk(f"Lan có {a} quyển vở. Mẹ mua thêm {b} quyển. Hỏi Lan có tất cả bao nhiêu quyển vở?", a + b, nw(a + b), f"Số vở có tất cả: {a} + {b} = {a+b} (quyển).", 1))
    for _ in range(3):
        a = R.randint(200, 900); b = R.randint(50, a - 50)
        out.append(mk(f"Cửa hàng có {a} kg gạo, đã bán {b} kg. Hỏi còn lại bao nhiêu ki-lô-gam gạo?", a - b, nw(a - b), f"Số gạo còn lại: {a} − {b} = {a-b} (kg).", 1))
    for _ in range(3):
        a, b = R.randint(6, 25), R.randint(4, 15)
        out.append(mk(f"Mỗi hộp có {a} cái kẹo. Hỏi {b} hộp như vậy có bao nhiêu cái kẹo?", a * b, nw(a * b), f"Số kẹo: {a} × {b} = {a*b} (cái).", 2))
    for _ in range(3):
        b, q = R.randint(3, 9), R.randint(5, 30)
        out.append(mk(f"Có {b*q} học sinh xếp đều thành {b} hàng. Hỏi mỗi hàng có bao nhiêu học sinh?", q, nw(q), f"Mỗi hàng có: {b*q} : {b} = {q} (học sinh).", 2))
    for _ in range(3):
        a, b = R.randint(10, 60), R.randint(5, 40)
        out.append(mk(f"Một mảnh vườn hình chữ nhật dài {a} m, rộng {b} m. Tính diện tích mảnh vườn.", f"{a*b} m²", [f"{(a+b)*2} m²", f"{a+b} m²", f"{a*b+a} m²"], f"Diện tích: {a} × {b} = {a*b} (m²).", 3))
    return out

def gen_units():
    T = [("m", "cm", 100), ("km", "m", 1000), ("kg", "g", 1000), ("giờ", "phút", 60), ("phút", "giây", 60), ("yến", "kg", 10), ("tạ", "kg", 100), ("tấn", "kg", 1000)]
    out = []
    for i in range(16):
        u, v, f = T[i % len(T)]; n = R.randint(2, 9); c = n * f
        out.append(mk(f"{n} {u} = … {v}", c, [c * 10, c // 10 if c % 10 == 0 else c + f, c + f, c - f if c > f else c + 2 * f], f"1 {u} = {f} {v} nên {n} {u} = {n} × {f} = {c} {v}.", 1 if f <= 100 else 2))
    return out

toan = [("Phép cộng", gen_add()), ("Phép trừ", gen_sub()), ("Phép nhân", gen_mul()), ("Phép chia", gen_div()),
        ("So sánh số", gen_compare()), ("Phân số", gen_frac()), ("Hình học", gen_geo()), ("Đại lượng", gen_units()), ("Giải toán có lời văn", gen_word())]

# ---------- CÁC MÔN KHÁC (soạn tay: câu, đáp án đúng, các đáp án sai, giải thích) ----------
def H(rows): return [tf(r[0], r[1], r[2]) if isinstance(r[1], bool) else mk(r[0], r[1], r[2], r[3]) for r in rows]

tv = [("Từ loại", H([
 ("Từ nào là danh từ?", "bàn", ["chạy", "đẹp", "nhanh"], "Danh từ chỉ sự vật. “Bàn” là đồ vật."),
 ("Từ nào là động từ?", "ăn", ["quyển vở", "xanh", "cô giáo"], "Động từ chỉ hoạt động. “Ăn” là hoạt động."),
 ("Từ nào là tính từ?", "cao", ["đọc", "trường", "bút"], "Tính từ chỉ đặc điểm, tính chất."),
 ("Trong câu “Bé đang chơi đùa ngoài sân.”, động từ là từ nào?", "chơi đùa", ["Bé", "ngoài sân", "sân"], "“Chơi đùa” chỉ hoạt động của bé."),
 ("Từ nào chỉ đặc điểm?", "xinh đẹp", ["học bài", "bác sĩ", "sách"], "“Xinh đẹp” nói về đặc điểm."),
 ("Từ nào chỉ hoạt động?", "bơi", ["bầu trời", "trắng", "nhà"], "“Bơi” là hoạt động."),
 ("Từ nào chỉ người?", "học sinh", ["bàn học", "cây bàng", "con gà"], "“Học sinh” là danh từ chỉ người."),
 ("“Mưa” là danh từ chỉ gì?", "hiện tượng tự nhiên", ["con vật", "đồ dùng", "người"], "Mưa là hiện tượng thiên nhiên."),
 ("Từ nào KHÔNG phải động từ?", "xanh", ["nhảy", "viết", "hát"], "“Xanh” chỉ màu sắc nên là tính từ."),
 ("Từ nào là danh từ chỉ con vật?", "con trâu", ["chăm chỉ", "chạy nhảy", "to lớn"], "“Con trâu” chỉ con vật."),
])), ("Từ đồng nghĩa – trái nghĩa", H([
 ("Từ trái nghĩa với “nhanh” là gì?", "chậm", ["mạnh", "giỏi", "đẹp"], "Nhanh và chậm có nghĩa ngược nhau."),
 ("Từ trái nghĩa với “sáng” là gì?", "tối", ["trắng", "cao", "xa"], "Sáng ↔ tối."),
 ("Từ trái nghĩa với “vui” là gì?", "buồn", ["cười", "hát", "mừng"], "Vui ↔ buồn."),
 ("Từ đồng nghĩa với “chăm chỉ” là gì?", "siêng năng", ["lười biếng", "vui vẻ", "nhanh nhẹn"], "Chăm chỉ = siêng năng."),
 ("Từ đồng nghĩa với “xinh đẹp” là gì?", "đẹp đẽ", ["xấu xí", "thấp bé", "ồn ào"], "Cùng nói về vẻ đẹp."),
 ("Từ trái nghĩa với “nóng” là gì?", "lạnh", ["khô", "cứng", "nhẹ"], "Nóng ↔ lạnh."),
 ("Từ đồng nghĩa với “bao la” là gì?", "mênh mông", ["chật hẹp", "nhỏ bé", "ngắn ngủi"], "Đều chỉ không gian rất rộng."),
 ("Từ trái nghĩa với “dũng cảm” là gì?", "hèn nhát", ["mạnh mẽ", "kiên cường", "thông minh"], "Dũng cảm ↔ hèn nhát."),
 ("Từ trái nghĩa với “trong” (nước trong) là gì?", "đục", ["sạch", "mát", "sâu"], "Nước trong ↔ nước đục."),
 ("Từ đồng nghĩa với “mẹ” là gì?", "má", ["ba", "anh", "chú"], "Mẹ, má, u, bầm... đều chỉ người sinh ra mình."),
])), ("Dấu câu và chính tả", H([
 ("Cuối câu hỏi ta dùng dấu gì?", "dấu chấm hỏi (?)", ["dấu chấm (.)", "dấu phẩy (,)", "dấu chấm than (!)"], "Câu hỏi kết thúc bằng dấu chấm hỏi."),
 ("Cuối câu cảm thán ta thường dùng dấu gì?", "dấu chấm than (!)", ["dấu chấm (.)", "dấu phẩy (,)", "dấu hai chấm (:)"], "Câu cảm thán bộc lộ cảm xúc, kết thúc bằng dấu chấm than."),
 ("Dấu phẩy dùng để làm gì?", "ngăn cách các bộ phận trong câu", ["kết thúc câu", "báo hiệu câu hỏi", "mở đầu đoạn văn"], "Dấu phẩy ngăn cách các từ, cụm từ trong câu."),
 ("Từ nào viết đúng chính tả?", "chăm chỉ", ["trăm chỉ", "chăm chĩ", "trăm chĩ"], "Viết đúng là “chăm chỉ”."),
 ("Từ nào viết đúng chính tả?", "xinh xắn", ["sinh xắn", "xinh sắn", "sinh sắn"], "Viết đúng là “xinh xắn”."),
 ("Từ nào viết đúng chính tả?", "ruộng lúa", ["duộng lúa", "giuộng lúa", "zuộng lúa"], "Viết đúng là “ruộng lúa”."),
 ("Từ nào viết đúng chính tả?", "giúp đỡ", ["dúp đỡ", "rúp đỡ", "giúp đở"], "Viết đúng là “giúp đỡ”."),
 ("Từ nào viết đúng chính tả?", "sáng sủa", ["sáng xủa", "xáng sủa", "sáng sũa"], "Viết đúng là “sáng sủa”."),
 ("Dấu hai chấm (:) thường dùng để làm gì?", "báo hiệu lời nói hoặc phần liệt kê", ["kết thúc câu hỏi", "nối hai từ", "ngắt nghỉ rất ngắn"], "Sau dấu hai chấm thường là lời nói hoặc các ý liệt kê."),
 ("Câu “Hôm nay trời đẹp quá” nên kết thúc bằng dấu nào?", "dấu chấm than (!)", ["dấu chấm hỏi (?)", "dấu hai chấm (:)", "dấu phẩy (,)"], "Đây là câu cảm thán."),
]))]

kh = [("Con người và sức khỏe", H([
 ("Cơ quan nào giúp chúng ta hít thở?", "phổi", ["tim", "dạ dày", "gan"], "Phổi giúp trao đổi khí."),
 ("Cơ quan nào bơm máu đi khắp cơ thể?", "tim", ["phổi", "thận", "não"], "Tim co bóp đẩy máu đi nuôi cơ thể."),
 ("Nên đánh răng ít nhất mấy lần mỗi ngày?", "2 lần", ["1 lần", "mỗi tuần 1 lần", "không cần"], "Sáng và tối giúp răng sạch, chắc khỏe."),
 ("Nhóm thức ăn nào giàu chất đạm?", "thịt, cá, trứng", ["cơm, bánh mì", "rau, củ", "dầu, mỡ"], "Chất đạm giúp cơ thể lớn lên và khỏe mạnh."),
 ("Thức ăn nào cung cấp nhiều vi-ta-min?", "rau, quả", ["kẹo", "nước ngọt", "mỡ"], "Rau và quả tươi giàu vi-ta-min và chất xơ."),
 ("Bộ phận nào điều khiển mọi hoạt động của cơ thể?", "não", ["xương", "da", "ruột"], "Não là trung tâm điều khiển."),
 ("Vì sao cần rửa tay trước khi ăn?", "để loại bỏ vi khuẩn", ["để tay thơm", "để tay to hơn", "không cần thiết"], "Tay bẩn có thể mang vi khuẩn gây bệnh."),
 ("Ngủ đủ giấc giúp em điều gì?", "khỏe mạnh và học tập tập trung", ["mau đói", "giảm chiều cao", "dễ ốm hơn"], "Ngủ đủ giúp cơ thể và trí óc nghỉ ngơi."),
 ("Ăn quá nhiều đồ ngọt có hại cho răng.", True, "Đồ ngọt dễ gây sâu răng."),
 ("Nguồn cung cấp năng lượng chính cho cơ thể là chất nào?", "chất bột đường", ["chất khoáng", "nước", "chất xơ"], "Cơm, bánh mì, khoai... cho nhiều năng lượng."),
])), ("Động vật và thực vật", H([
 ("Cây xanh hấp thụ khí nào để quang hợp?", "khí các-bô-níc", ["khí ôxi", "khí ni-tơ", "khí hy-đrô"], "Cây dùng khí các-bô-níc và ánh sáng để tạo chất dinh dưỡng."),
 ("Bộ phận nào của cây hút nước từ đất?", "rễ", ["lá", "hoa", "quả"], "Rễ hút nước và muối khoáng."),
 ("Bộ phận nào của cây chủ yếu làm nhiệm vụ quang hợp?", "lá", ["rễ", "thân", "hạt"], "Lá có chất diệp lục nên quang hợp."),
 ("Động vật nào đẻ trứng?", "gà", ["mèo", "chó", "bò"], "Gà là loài chim, đẻ trứng."),
 ("Động vật nào là loài thú?", "con voi", ["chim sẻ", "cá chép", "con ếch"], "Thú đẻ con và nuôi con bằng sữa."),
 ("Con vật nào ăn cỏ?", "con trâu", ["sư tử", "hổ", "cá mập"], "Trâu là động vật ăn cỏ."),
 ("Cá thở bằng bộ phận nào?", "mang", ["phổi", "mũi", "lông"], "Cá lấy ôxi trong nước nhờ mang."),
 ("Hạt nảy mầm cần những gì?", "nước, không khí và nhiệt độ thích hợp", ["chỉ cần ánh sáng", "chỉ cần đất", "chỉ cần phân bón"], "Đó là các điều kiện cần cho hạt nảy mầm."),
 ("Con dơi là loài chim.", False, "Dơi đẻ con và nuôi con bằng sữa nên là loài thú."),
 ("Chuỗi thức ăn nào đúng?", "Cỏ → Châu chấu → Ếch", ["Ếch → Cỏ → Châu chấu", "Châu chấu → Ếch → Cỏ", "Cỏ → Ếch → Châu chấu"], "Sinh vật này là thức ăn của sinh vật kế tiếp."),
])), ("Nước, không khí và năng lượng", H([
 ("Nước sôi ở bao nhiêu độ C?", "100", ["50", "80", "120"], "Ở điều kiện bình thường, nước sôi ở 100 độ C."),
 ("Nước đá là nước ở thể rắn.", True, "Nước đông lại ở 0 độ C thành nước đá."),
 ("Nước có tính chất nào?", "không màu, không mùi, không vị", ["màu xanh", "mùi thơm", "vị ngọt"], "Nước tinh khiết không màu, không mùi, không vị."),
 ("Con người cần khí nào để thở?", "ôxi", ["ni-tơ", "các-bô-níc", "hy-đrô"], "Ôxi giúp cơ thể sống và hoạt động."),
 ("Không khí có màu.", False, "Không khí trong suốt, không màu, không mùi."),
 ("Nguồn năng lượng chính của Trái Đất là gì?", "Mặt Trời", ["Mặt Trăng", "gió", "than đá"], "Mặt Trời cho ánh sáng và nhiệt."),
 ("Hơi nước gặp lạnh biến thành giọt nước gọi là gì?", "ngưng tụ", ["bay hơi", "đông đặc", "nóng chảy"], "Hơi nước → nước lỏng gọi là ngưng tụ."),
 ("Nước biến thành hơi nước gọi là gì?", "bay hơi", ["ngưng tụ", "đông đặc", "nóng chảy"], "Nước lỏng → hơi nước gọi là bay hơi."),
 ("Nguồn năng lượng nào có thể tái tạo?", "gió", ["than đá", "dầu mỏ", "khí đốt"], "Gió, nắng không bị cạn kiệt."),
 ("Để tiết kiệm nước, em nên làm gì?", "khóa vòi khi không dùng", ["mở vòi chảy liên tục", "xả nước chơi", "rửa tay thật lâu"], "Khóa vòi giúp tiết kiệm nước."),
 ("Âm thanh được tạo ra khi vật như thế nào?", "rung động", ["đứng yên", "nóng lên", "lạnh đi"], "Vật rung động tạo ra âm thanh."),
 ("Vật nào là vật cách điện?", "nhựa", ["đồng", "sắt", "nhôm"], "Kim loại dẫn điện, nhựa thì không."),
]))]

ls = [("Địa lý Việt Nam", H([
 ("Thủ đô của Việt Nam là gì?", "Hà Nội", ["Huế", "Đà Nẵng", "TP. Hồ Chí Minh"], "Hà Nội là thủ đô của nước ta."),
 ("Dãy núi cao nhất Việt Nam là gì?", "Hoàng Liên Sơn", ["Trường Sơn", "Bạch Mã", "Tam Đảo"], "Đỉnh Phan-xi-păng thuộc dãy Hoàng Liên Sơn."),
 ("Đồng bằng lớn nhất ở miền Bắc là gì?", "Đồng bằng sông Hồng", ["Đồng bằng sông Cửu Long", "Tây Nguyên", "Đồng bằng duyên hải miền Trung"], "Sông Hồng bồi đắp nên đồng bằng Bắc Bộ."),
 ("Sông Cửu Long chảy qua vùng Nam Bộ.", True, "Đồng bằng sông Cửu Long ở Nam Bộ."),
 ("Tây Nguyên nổi tiếng với cây gì?", "cà phê", ["cây dừa", "hoa anh đào", "cây thốt nốt"], "Tây Nguyên trồng nhiều cà phê."),
 ("Thành phố đông dân nhất nước ta là gì?", "TP. Hồ Chí Minh", ["Huế", "Đà Nẵng", "Cần Thơ"], "TP. Hồ Chí Minh có dân số đông nhất cả nước."),
 ("Vịnh Hạ Long thuộc tỉnh nào?", "Quảng Ninh", ["Khánh Hòa", "Kiên Giang", "Bình Định"], "Vịnh Hạ Long ở Quảng Ninh."),
 ("Biển Đông nằm ở phía nào của nước ta?", "phía đông", ["phía tây", "phía bắc", "phía nam"], "Biển Đông ở phía đông và nam nước ta."),
 ("Việt Nam có đường bờ biển dài.", True, "Bờ biển nước ta dài hơn 3 260 km."),
 ("Cố đô Huế thuộc miền nào?", "miền Trung", ["miền Bắc", "miền Nam", "Tây Bắc"], "Huế nằm ở miền Trung."),
 ("Đà Nẵng thuộc miền nào?", "miền Trung", ["miền Bắc", "miền Nam", "Tây Bắc"], "Đà Nẵng nằm ở duyên hải miền Trung."),
 ("Đồng bằng sông Cửu Long được gọi là gì?", "vựa lúa của cả nước", ["vựa cà phê", "vựa chè", "vựa muối"], "Nơi đây sản xuất nhiều lúa gạo nhất."),
])), ("Lịch sử Việt Nam", H([
 ("Các vua Hùng dựng nên nước nào?", "Văn Lang", ["Âu Lạc", "Đại Việt", "Đại Cồ Việt"], "Nhà nước đầu tiên của người Việt là Văn Lang."),
 ("Ngô Quyền đánh thắng quân Nam Hán trên sông nào?", "sông Bạch Đằng", ["sông Hồng", "sông Cửu Long", "sông Mã"], "Chiến thắng Bạch Đằng năm 938."),
 ("Hai Bà Trưng khởi nghĩa chống quân nào?", "quân Hán", ["quân Mông – Nguyên", "quân Minh", "quân Thanh"], "Năm 40, Hai Bà Trưng đánh quân nhà Hán."),
 ("Vị vua dời đô về Thăng Long là ai?", "Lý Thái Tổ", ["Lê Lợi", "Trần Hưng Đạo", "Ngô Quyền"], "Năm 1010, Lý Thái Tổ dời đô về Thăng Long."),
 ("Trần Hưng Đạo lãnh đạo kháng chiến chống quân nào?", "quân Mông – Nguyên", ["quân Minh", "quân Thanh", "quân Hán"], "Ba lần đánh thắng quân Mông – Nguyên."),
 ("Lê Lợi lãnh đạo khởi nghĩa Lam Sơn chống quân nào?", "quân Minh", ["quân Thanh", "quân Tống", "quân Hán"], "Khởi nghĩa Lam Sơn chống quân Minh."),
 ("Kinh đô được đặt tên là Thăng Long vào năm nào?", "1010", ["938", "1288", "1428"], "Năm 1010 Lý Thái Tổ dời đô và đặt tên Thăng Long."),
 ("Quang Trung đại phá quân Thanh vào năm nào?", "1789", ["1010", "1075", "1945"], "Chiến thắng Ngọc Hồi – Đống Đa năm 1789."),
 ("Chiến thắng Điện Biên Phủ diễn ra năm 1954.", True, "Chiến thắng Điện Biên Phủ năm 1954."),
 ("Quốc khánh nước ta là ngày nào?", "2 tháng 9", ["30 tháng 4", "1 tháng 5", "19 tháng 8"], "Ngày 2/9/1945 Bác Hồ đọc Tuyên ngôn Độc lập."),
])), ("Văn hóa và danh lam", H([
 ("Tết Trung thu thường có hoạt động nào?", "rước đèn, phá cỗ", ["bắn pháo hoa giao thừa", "tảo mộ", "gói bánh chưng"], "Trung thu là Tết của thiếu nhi."),
 ("Bánh chưng thường được gói vào dịp nào?", "Tết Nguyên đán", ["Tết Trung thu", "Tết Đoan Ngọ", "Giỗ Tổ"], "Bánh chưng là món truyền thống ngày Tết."),
 ("Quan họ là dân ca của vùng nào?", "Bắc Ninh", ["Huế", "Cần Thơ", "Đà Lạt"], "Dân ca quan họ là di sản của Bắc Ninh."),
 ("Giỗ Tổ Hùng Vương là ngày nào?", "10 tháng 3 âm lịch", ["1 tháng 1", "15 tháng 8", "5 tháng 5"], "“Dù ai đi ngược về xuôi, nhớ ngày giỗ Tổ mùng mười tháng ba.”"),
 ("Văn Miếu – Quốc Tử Giám ở thành phố nào?", "Hà Nội", ["Huế", "Hải Phòng", "Cần Thơ"], "Đây là trường đại học đầu tiên của nước ta."),
 ("Cồng chiêng là nhạc cụ nổi tiếng của vùng nào?", "Tây Nguyên", ["Đồng bằng Bắc Bộ", "Nam Bộ", "Duyên hải miền Trung"], "Không gian văn hóa cồng chiêng Tây Nguyên là di sản thế giới."),
 ("Trang phục truyền thống của người Việt là gì?", "áo dài", ["kimono", "hanbok", "sari"], "Áo dài là trang phục truyền thống Việt Nam."),
 ("Đền Hùng ở tỉnh nào?", "Phú Thọ", ["Hà Nam", "Yên Bái", "Nghệ An"], "Đền Hùng thuộc tỉnh Phú Thọ."),
]))]

en = [("Animals & Colors", H([
 ("“Cat” nghĩa là gì?", "con mèo", ["con chó", "con gà", "con cá"], "Cat = con mèo."),
 ("“Dog” nghĩa là gì?", "con chó", ["con mèo", "con gà", "con cá"], "Dog = con chó."),
 ("“Bird” nghĩa là gì?", "con chim", ["con bò", "con voi", "con khỉ"], "Bird = con chim."),
 ("“Elephant” nghĩa là gì?", "con voi", ["con thỏ", "con khỉ", "con hổ"], "Elephant = con voi."),
 ("“Rabbit” nghĩa là gì?", "con thỏ", ["con voi", "con khỉ", "con vịt"], "Rabbit = con thỏ."),
 ("“Con cá” trong tiếng Anh là gì?", "fish", ["bird", "cat", "cow"], "Fish = con cá."),
 ("“Con bò” trong tiếng Anh là gì?", "cow", ["duck", "pig", "horse"], "Cow = con bò."),
 ("“Red” là màu gì?", "đỏ", ["xanh dương", "vàng", "tím"], "Red = màu đỏ."),
 ("“Blue” là màu gì?", "xanh dương", ["đỏ", "vàng", "đen"], "Blue = xanh dương."),
 ("“Yellow” là màu gì?", "vàng", ["xanh lá", "trắng", "hồng"], "Yellow = màu vàng."),
 ("Snow is ____.", "white", ["black", "green", "pink"], "Tuyết màu trắng (white)."),
 ("The banana is ____.", "yellow", ["blue", "purple", "gray"], "Chuối chín màu vàng (yellow)."),
])), ("Numbers & Family", H([
 ("“Five” là số mấy?", "5", ["4", "6", "15"], "Five = 5."),
 ("“Ten” là số mấy?", "10", ["1", "9", "20"], "Ten = 10."),
 ("“Seven” là số mấy?", "7", ["6", "8", "17"], "Seven = 7."),
 ("Số 8 trong tiếng Anh là gì?", "eight", ["six", "nine", "eighteen"], "8 = eight."),
 ("Số 9 trong tiếng Anh là gì?", "nine", ["five", "ten", "nineteen"], "9 = nine."),
 ("Two + three = ?", "five", ["four", "six", "seven"], "2 + 3 = 5 (five)."),
 ("“Mother” nghĩa là gì?", "mẹ", ["bố", "chị", "bà"], "Mother = mẹ."),
 ("“Father” nghĩa là gì?", "bố", ["mẹ", "anh", "ông"], "Father = bố."),
 ("“Sister” nghĩa là gì?", "chị/em gái", ["anh/em trai", "bà", "cô"], "Sister = chị hoặc em gái."),
 ("“Brother” nghĩa là gì?", "anh/em trai", ["chị/em gái", "ông", "chú"], "Brother = anh hoặc em trai."),
 ("“Grandmother” nghĩa là gì?", "bà", ["mẹ", "cô", "dì"], "Grandmother = bà."),
 ("“Ông” trong tiếng Anh là gì?", "grandfather", ["father", "brother", "uncle"], "Grandfather = ông."),
])), ("School & Food", H([
 ("“Book” nghĩa là gì?", "quyển sách", ["cái bút", "cái bàn", "cái ghế"], "Book = quyển sách."),
 ("“Pencil” nghĩa là gì?", "bút chì", ["bút mực", "thước kẻ", "cục tẩy"], "Pencil = bút chì."),
 ("“Teacher” nghĩa là gì?", "giáo viên", ["học sinh", "bác sĩ", "công an"], "Teacher = giáo viên."),
 ("“Desk” nghĩa là gì?", "bàn học", ["ghế", "bảng", "cửa sổ"], "Desk = bàn học."),
 ("“Cái cặp” trong tiếng Anh là gì?", "school bag", ["ruler", "eraser", "notebook"], "School bag = cặp sách."),
 ("“Rice” nghĩa là gì?", "cơm/gạo", ["bánh mì", "sữa", "nước"], "Rice = cơm, gạo."),
 ("“Bread” nghĩa là gì?", "bánh mì", ["cơm", "trứng", "cá"], "Bread = bánh mì."),
 ("“Milk” nghĩa là gì?", "sữa", ["nước", "trà", "nước cam"], "Milk = sữa."),
 ("“Apple” nghĩa là gì?", "quả táo", ["quả chuối", "quả cam", "quả nho"], "Apple = quả táo."),
 ("“Nước” trong tiếng Anh là gì?", "water", ["milk", "juice", "tea"], "Water = nước."),
 ("“Quả chuối” trong tiếng Anh là gì?", "banana", ["apple", "orange", "grape"], "Banana = quả chuối."),
 ("“Trứng” trong tiếng Anh là gì?", "egg", ["fish", "meat", "rice"], "Egg = quả trứng."),
])), ("Grammar cơ bản", H([
 ("I ____ a student.", "am", ["is", "are", "be"], "Với “I” ta dùng “am”."),
 ("She ____ my sister.", "is", ["am", "are", "be"], "Với “she” ta dùng “is”."),
 ("They ____ happy.", "are", ["is", "am", "be"], "Với “they” ta dùng “are”."),
 ("There ____ a book on the desk.", "is", ["are", "am", "be"], "Một quyển sách (số ít) → “is”."),
 ("This is ____ apple.", "an", ["a", "the", "two"], "Trước nguyên âm (a, e, i, o, u) dùng “an”."),
 ("How are you? – I'm ____.", "fine, thank you", ["I'm a book", "yes, I do", "blue"], "Trả lời lịch sự khi được hỏi thăm."),
 ("What's your name? – ____ Lan.", "My name is", ["I have", "You are", "She is"], "Giới thiệu tên: “My name is …”."),
 ("He ____ football every day.", "plays", ["play", "playing", "to play"], "Chủ ngữ “he” → động từ thêm “s”."),
 ("How old are you? – I'm nine ____ old.", "years", ["year", "yearly", "age"], "I'm nine years old = Tôi chín tuổi."),
 ("Good morning! nghĩa là gì?", "Chào buổi sáng!", ["Chúc ngủ ngon!", "Tạm biệt!", "Cảm ơn!"], "Good morning = Chào buổi sáng."),
]))]

bank = []
for name, topics in [("Toán", toan), ("Tiếng Việt", tv), ("Khoa học", kh), ("Lịch sử – Địa lý", ls), ("Tiếng Anh", en)]:
    bank.append(dict(name=name, icon=COL[name][0], color=COL[name][1],
                     topics=[dict(name=t, questions=qs) for t, qs in topics]))
# kiểm tra
tot = 0
for s in bank:
    for t in s["topics"]:
        for q in t["questions"]:
            assert 2 <= len(q["options"]) <= 4 and len(set(q["options"])) == len(q["options"]), q
            assert 0 <= q["correct_index"] < len(q["options"]), q
            tot += 1
        print(f'{s["name"]:18} {t["name"]:32} {len(t["questions"])}')
print("TOTAL", tot)
import os
os.makedirs("android/app/src/main/assets", exist_ok=True)
json.dump(bank, open("android/app/src/main/assets/question_bank.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
