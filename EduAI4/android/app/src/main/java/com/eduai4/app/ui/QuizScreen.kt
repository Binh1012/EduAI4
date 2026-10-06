package com.eduai4.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.lifecycle.viewmodel.compose.viewModel
import com.eduai4.app.viewmodel.QuizViewModel

@Composable
fun QuizScreen(topicId: Int, onExit: () -> Unit, vm: QuizViewModel = viewModel()) {
    val ui by vm.ui.collectAsState()
    LaunchedEffect(topicId) { vm.load(topicId) }

    when {
        ui.loading || ui.submitting -> LoadingView()
        ui.error != null -> ErrorView(ui.error!!, onRetry = vm::retry)
        ui.result != null -> ResultView(vm, onExit, topicId)
        else -> QuestionView(vm, onExit)
    }
}

@Composable
private fun QuestionView(vm: QuizViewModel, onExit: () -> Unit) {
    val ui by vm.ui.collectAsState()
    val q = ui.questions[ui.index]
    val selected = ui.selected
    val isLast = ui.index + 1 == ui.questions.size

    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)) {
        TextButton(onClick = onExit) { Text("✕ Thoát", fontSize = 18.sp) }
        Text("Câu ${ui.index + 1}/${ui.questions.size}", fontWeight = FontWeight.Bold, fontSize = 18.sp)
        Spacer(Modifier.height(6.dp))
        LinearProgressIndicator(
            progress = { ui.index / ui.questions.size.toFloat() },
            modifier = Modifier.fillMaxWidth().height(12.dp),
        )
        Spacer(Modifier.height(16.dp))
        AppCard { Text(q.text, fontSize = 22.sp, fontWeight = FontWeight.Bold) }
        Spacer(Modifier.height(14.dp))

        q.options.forEachIndexed { i, option ->
            val bg = when {
                selected == null -> Color.White
                i == q.correct_index -> OkBg
                i == selected -> BadBg
                else -> Color.White
            }
            val border = when {
                selected == null -> Color.Transparent
                i == q.correct_index -> Ok
                i == selected -> Bad
                else -> Color.Transparent
            }
            OutlinedButton(
                onClick = { vm.select(i) },
                enabled = selected == null,
                modifier = Modifier.fillMaxWidth().heightIn(min = 64.dp).padding(bottom = 10.dp),
                shape = RoundedCornerShape(18.dp),
                border = androidx.compose.foundation.BorderStroke(3.dp, border),
                colors = ButtonDefaults.outlinedButtonColors(
                    containerColor = bg, contentColor = Ink, disabledContainerColor = bg, disabledContentColor = Ink,
                ),
            ) {
                Text("${"ABCD"[i]}. $option", fontSize = 20.sp, modifier = Modifier.fillMaxWidth())
            }
        }

        if (selected != null) {
            val right = selected == q.correct_index
            AppCard(Modifier.padding(top = 4.dp)) {
                Text(if (right) "🎉 Chính xác!" else "💡 Chưa đúng rồi! Hãy thử xem lại nhé.", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                if (q.explanation.isNotBlank()) Text(q.explanation, fontSize = 18.sp)
            }
            Spacer(Modifier.height(8.dp))
            BigButton(if (isLast) "Xem kết quả" else "Câu tiếp theo", vm::next)
        }
    }
}

@Composable
private fun ResultView(vm: QuizViewModel, onExit: () -> Unit, topicId: Int) {
    val ui by vm.ui.collectAsState()
    val r = ui.result!!
    val wrong = ui.questions.zip(ui.answers).filter { (q, a) -> a.selected != q.correct_index }

    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Text(if (r.percent >= 80) "🎉" else if (r.percent >= 50) "👍" else "💪", fontSize = 72.sp)
        Text("Hoàn thành!", fontSize = 32.sp, fontWeight = FontWeight.ExtraBold)
        Text("${r.correct}/${r.total} • ${r.percent}%", fontSize = 36.sp, fontWeight = FontWeight.ExtraBold)
        Text("+${r.xp_gained} XP", fontSize = 20.sp)
        Spacer(Modifier.height(16.dp))
        if (wrong.isEmpty()) {
            AppCard { Text("Em trả lời đúng hết! ⭐", fontSize = 20.sp, textAlign = TextAlign.Center) }
        } else {
            Text("Các câu cần xem lại", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.align(Alignment.Start))
            Spacer(Modifier.height(8.dp))
            wrong.forEach { (q, _) ->
                AppCard(Modifier.padding(bottom = 10.dp)) {
                    Text(q.text, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Đáp án: ${q.options[q.correct_index]}", fontSize = 18.sp, color = Ok)
                    if (q.explanation.isNotBlank()) Text(q.explanation, fontSize = 16.sp)
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        BigButton("Làm lại", { vm.load(topicId) })
        Spacer(Modifier.height(8.dp))
        BigButton("Về trang chủ", onExit, container = Color.White, content = Ink)
    }
}
