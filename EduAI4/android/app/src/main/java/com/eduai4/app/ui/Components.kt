package com.eduai4.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.eduai4.app.viewmodel.UiState

fun parseColor(hex: String): Color =
    try { Color(android.graphics.Color.parseColor(hex)) } catch (_: Exception) { Color(0xFF2F7BFF) }

@Composable
fun BigButton(
    text: String, onClick: () -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true,
    container: Color = MaterialTheme.colorScheme.primary, content: Color = Color.White,
) = Button(
    onClick = onClick, enabled = enabled,
    modifier = modifier.fillMaxWidth().heightIn(min = 56.dp),
    shape = RoundedCornerShape(18.dp),
    colors = ButtonDefaults.buttonColors(containerColor = container, contentColor = content),
) { Text(text, fontSize = 20.sp, fontWeight = FontWeight.Bold) }

@Composable
fun AppCard(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) = Card(
    modifier = modifier.fillMaxWidth(),
    shape = RoundedCornerShape(20.dp),
    colors = CardDefaults.cardColors(containerColor = Color.White),
) { Column(Modifier.padding(16.dp), content = content) }

@Composable
fun LoadingView() = Box(Modifier.fillMaxSize(), Alignment.Center) { CircularProgressIndicator() }

@Composable
fun ErrorView(message: String, onRetry: () -> Unit) = Column(
    Modifier.fillMaxSize().padding(24.dp), Arrangement.Center, Alignment.CenterHorizontally,
) {
    Text("😕", fontSize = 56.sp)
    Spacer(Modifier.height(8.dp))
    Text(message, fontSize = 18.sp, textAlign = TextAlign.Center)
    Spacer(Modifier.height(16.dp))
    BigButton("Thử lại", onRetry)
}

@Composable
fun EmptyView(message: String) = Box(Modifier.fillMaxSize().padding(24.dp), Alignment.Center) {
    Text(message, fontSize = 18.sp, textAlign = TextAlign.Center)
}

@Composable
fun <T> StateView(state: UiState<T>, onRetry: () -> Unit, content: @Composable (T) -> Unit) {
    when (state) {
        UiState.Loading -> LoadingView()
        is UiState.Error -> ErrorView(state.message, onRetry)
        is UiState.Success -> content(state.data)
    }
}
