package com.eduai4.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.eduai4.app.data.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed interface UiState<out T> {
    data object Loading : UiState<Nothing>
    data class Error(val message: String) : UiState<Nothing>
    data class Success<T>(val data: T) : UiState<T>
}

fun <T> Result<T>.toState(): UiState<T> =
    fold({ UiState.Success(it) }, { UiState.Error(it.message ?: "Có lỗi xảy ra") })

class AuthViewModel : ViewModel() {
    private val repo = Graph.repo
    val loggedIn = MutableStateFlow(Graph.session.token != null)
    val loading = MutableStateFlow(false)
    val error = MutableStateFlow<String?>(null)

    fun login(email: String, password: String) = run { repo.login(email.trim(), password) }
    fun register(name: String, email: String, password: String) = run { repo.register(name.trim(), email.trim(), password) }
    fun clearError() { error.value = null }

    fun logout() {
        viewModelScope.launch { repo.logout(); loggedIn.value = false }
    }

    private fun run(block: suspend () -> Result<Unit>) {
        viewModelScope.launch {
            loading.value = true
            error.value = null
            block().fold({ loggedIn.value = true }, { error.value = it.message })
            loading.value = false
        }
    }
}

/** Shared by Home, Subject and Progress screens. */
class MainViewModel : ViewModel() {
    private val repo = Graph.repo
    val subjects = MutableStateFlow<UiState<List<SubjectDto>>>(UiState.Loading)
    val progress = MutableStateFlow<UiState<ProgressDto>>(UiState.Loading)
    val recommend = MutableStateFlow<RecommendDto?>(null)

    fun load() {
        viewModelScope.launch {
            if (subjects.value !is UiState.Success) subjects.value = UiState.Loading
            if (progress.value !is UiState.Success) progress.value = UiState.Loading
            subjects.value = repo.subjects().toState()
            progress.value = repo.progress().toState()
            recommend.value = repo.recommend().getOrNull()
        }
    }

    fun clear() {
        subjects.value = UiState.Loading
        progress.value = UiState.Loading
        recommend.value = null
    }
}

class QuizViewModel : ViewModel() {
    private val repo = Graph.repo

    data class Ui(
        val loading: Boolean = true,
        val error: String? = null,
        val questions: List<QuestionDto> = emptyList(),
        val index: Int = 0,
        val selected: Int? = null,
        val answers: List<AnswerReq> = emptyList(),
        val submitting: Boolean = false,
        val result: ResultDto? = null,
    )

    val ui = MutableStateFlow(Ui())
    private var topicId = 0

    fun load(id: Int) {
        topicId = id
        ui.value = Ui()
        viewModelScope.launch {
            repo.questions(id).fold(
                { q ->
                    ui.value = if (q.isEmpty()) Ui(loading = false, error = "Chủ đề này chưa có câu hỏi.")
                    else Ui(loading = false, questions = q)
                },
                { ui.value = Ui(loading = false, error = it.message) },
            )
        }
    }

    fun select(i: Int) {
        if (ui.value.selected == null) ui.update { it.copy(selected = i) }
    }

    fun next() {
        val s = ui.value
        val sel = s.selected ?: return
        val answers = s.answers + AnswerReq(s.questions[s.index].id, sel)
        if (s.index + 1 < s.questions.size) {
            ui.value = s.copy(index = s.index + 1, selected = null, answers = answers)
        } else {
            ui.value = s.copy(answers = answers)
            submit()
        }
    }

    /** Also used as the "retry" action when sending the result failed. */
    fun submit() {
        val s = ui.value
        ui.value = s.copy(submitting = true, error = null)
        viewModelScope.launch {
            repo.submit(SubmitReq(topicId, s.answers)).fold(
                { r -> ui.update { it.copy(submitting = false, result = r) } },
                { e -> ui.update { it.copy(submitting = false, error = e.message) } },
            )
        }
    }

    fun retry() {
        val s = ui.value
        if (s.questions.isNotEmpty() && s.answers.size == s.questions.size) submit() else load(topicId)
    }
}

class TutorViewModel : ViewModel() {
    private val repo = Graph.repo
    val messages = MutableStateFlow(listOf(ChatMsg(false, "Hôm nay em muốn hỏi gì? 😊")))
    val sending = MutableStateFlow(false)

    fun send(text: String) {
        val q = text.trim()
        if (q.isEmpty() || sending.value) return
        messages.update { it + ChatMsg(true, q) }
        sending.value = true
        viewModelScope.launch {
            val reply = repo.tutor(q).getOrElse { it.message ?: "Cô chưa trả lời được lúc này." }
            messages.update { it + ChatMsg(false, reply) }
            sending.value = false
        }
    }
}
