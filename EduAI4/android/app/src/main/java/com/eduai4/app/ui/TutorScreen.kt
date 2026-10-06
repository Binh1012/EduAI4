package com.eduai4.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.eduai4.app.viewmodel.TutorViewModel

@Composable
fun TutorScreen(vm: TutorViewModel) {
    val messages by vm.messages.collectAsState()
    val sending by vm.sending.collectAsState()
    var text by remember { mutableStateOf("") }
    val listState = rememberLazyListState()
    LaunchedEffect(messages.size) { listState.animateScrollToItem(messages.lastIndex) }

    Column(Modifier.fillMaxSize().imePadding()) {
        LazyColumn(Modifier.weight(1f).padding(horizontal = 16.dp), state = listState, verticalArrangement = Arrangement.spacedBy(8.dp)) {
            item { Spacer(Modifier.height(8.dp)) }
            items(messages) { m ->
                Box(Modifier.fillMaxWidth(), contentAlignment = if (m.fromUser) Alignment.CenterEnd else Alignment.CenterStart) {
                    Text(
                        m.text, fontSize = 18.sp,
                        color = if (m.fromUser) Color.White else Ink,
                        modifier = Modifier.widthIn(max = 300.dp).clip(RoundedCornerShape(18.dp))
                            .background(if (m.fromUser) Color(0xFF2F7BFF) else Color.White).padding(12.dp),
                    )
                }
            }
            if (sending) item { Text("Cô đang suy nghĩ... 🤔", fontSize = 16.sp) }
        }
        Row(Modifier.fillMaxWidth().padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(
                text, { if (it.length <= 300) text = it }, modifier = Modifier.weight(1f),
                placeholder = { Text("Cô ơi, em muốn hỏi...") }, maxLines = 3,
            )
            Spacer(Modifier.width(8.dp))
            Button(onClick = { vm.send(text); text = "" }, enabled = text.isNotBlank() && !sending, modifier = Modifier.heightIn(min = 56.dp)) {
                Text("Gửi", fontSize = 18.sp)
            }
        }
    }
}
