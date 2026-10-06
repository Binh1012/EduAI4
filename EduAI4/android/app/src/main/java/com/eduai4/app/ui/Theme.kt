package com.eduai4.app.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val Ink = Color(0xFF1B2A4A)
val Ok = Color(0xFF2EB872)
val OkBg = Color(0xFFDCF7E8)
val Bad = Color(0xFFFF6B6B)
val BadBg = Color(0xFFFFE3E3)

private val Scheme = lightColorScheme(
    primary = Color(0xFF2F7BFF), onPrimary = Color.White,
    background = Color(0xFFEAF4FF), onBackground = Ink,
    surface = Color.White, onSurface = Ink,
)

@Composable
fun EduTheme(content: @Composable () -> Unit) = MaterialTheme(colorScheme = Scheme, content = content)
