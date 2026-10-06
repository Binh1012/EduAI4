package com.eduai4.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.eduai4.app.data.Graph
import com.eduai4.app.data.SubjectDto
import com.eduai4.app.viewmodel.MainViewModel
import com.eduai4.app.viewmodel.UiState

@Composable
fun HomeScreen(main: MainViewModel, onSubject: (Int) -> Unit, onTopic: (Int) -> Unit) {
    val subjects by main.subjects.collectAsState()
    val progress by main.progress.collectAsState()
    val rec by main.recommend.collectAsState()
    LaunchedEffect(Unit) { main.load() }

    StateView(subjects, onRetry = { main.load() }) { list ->
        if (list.isEmpty()) return@StateView EmptyView("Chưa có môn học nào.")
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)) {
            Text("Xin chào, ${Graph.session.name} 👋", fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            (progress as? UiState.Success)?.data?.let { p ->
                Spacer(Modifier.height(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatBox("⭐ ${p.xp}", "XP", Modifier.weight(1f))
                    StatBox("🚀 ${p.level}", "Cấp độ", Modifier.weight(1f))
                    StatBox("🔥 ${p.streak}", "Ngày liên tiếp", Modifier.weight(1f))
                }
            }
            rec?.let { r ->
                Spacer(Modifier.height(12.dp))
                AppCard {
                    Text("🤖 Gợi ý hôm nay", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text(r.message, fontSize = 18.sp)
                    r.topic_id?.let { id -> Spacer(Modifier.height(8.dp)); BigButton("Bắt đầu học", { onTopic(id) }) }
                }
            }
            Spacer(Modifier.height(16.dp))
            Text("Chọn môn học", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(8.dp))
            list.chunked(2).forEach { row ->
                Row(Modifier.padding(bottom = 12.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    row.forEach { SubjectCard(it, Modifier.weight(1f)) { onSubject(it.id) } }
                    if (row.size == 1) Spacer(Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun StatBox(value: String, label: String, modifier: Modifier) = Column(
    modifier.clip(RoundedCornerShape(16.dp)).background(Color.White).padding(10.dp),
    horizontalAlignment = Alignment.CenterHorizontally,
) {
    Text(value, fontWeight = FontWeight.Bold, fontSize = 20.sp)
    Text(label, fontSize = 13.sp)
}

@Composable
private fun SubjectCard(s: SubjectDto, modifier: Modifier, onClick: () -> Unit) = Column(
    modifier.heightIn(min = 112.dp).clip(RoundedCornerShape(22.dp)).background(parseColor(s.color))
        .clickable(onClick = onClick).padding(12.dp),
    Arrangement.Center, Alignment.CenterHorizontally,
) {
    Text(s.icon, fontSize = 40.sp)
    Text(s.name, color = Color.White, fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, textAlign = TextAlign.Center)
}

@Composable
fun SubjectScreen(main: MainViewModel, subjectId: Int, onBack: () -> Unit, onTopic: (Int) -> Unit) {
    val subjects by main.subjects.collectAsState()
    StateView(subjects, onRetry = { main.load() }) { list ->
        val s = list.find { it.id == subjectId } ?: return@StateView EmptyView("Không tìm thấy môn học.")
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)) {
            TextButton(onClick = onBack) { Text("← Quay lại", fontSize = 18.sp) }
            Text("${s.icon} ${s.name}", fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(12.dp))
            if (s.topics.isEmpty()) EmptyView("Môn này chưa có chủ đề.")
            s.topics.forEach { t ->
                AppCard(Modifier.padding(bottom = 10.dp).clickable { onTopic(t.id) }) {
                    Text(t.name, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    Text(if (t.accuracy == null) "Chưa làm bài" else "Đúng ${t.accuracy}%", fontSize = 16.sp)
                }
            }
        }
    }
}
