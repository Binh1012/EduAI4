package com.eduai4.app.data

// Field names match the JSON returned by the FastAPI backend (snake_case).
data class RegisterReq(val email: String, val name: String, val password: String)
data class LoginReq(val email: String, val password: String)
data class TokenRes(val access_token: String, val name: String, val role: String)

data class TopicDto(val id: Int, val name: String, val accuracy: Int?)
data class SubjectDto(val id: Int, val name: String, val icon: String, val color: String, val topics: List<TopicDto>)

data class QuestionDto(val id: Int, val text: String, val options: List<String>, val correct_index: Int, val explanation: String)
data class AnswerReq(val question_id: Int, val selected: Int)
data class SubmitReq(val topic_id: Int, val answers: List<AnswerReq>)
data class ResultDto(val correct: Int, val total: Int, val percent: Int, val xp_gained: Int)

data class TopicStat(val topic_id: Int, val topic: String, val subject: String, val accuracy: Int, val total: Int)
data class SubjectStat(val subject: String, val accuracy: Int?)
data class ProgressDto(
    val xp: Int, val level: Int, val streak: Int, val quizzes_done: Int, val perfect_quizzes: Int,
    val subjects: List<SubjectStat>, val weak_topics: List<TopicStat>,
)
data class RecommendDto(val topic_id: Int?, val topic: String?, val message: String)

data class TutorReq(val question: String)
data class TutorRes(val answer: String)
data class ChatMsg(val fromUser: Boolean, val text: String)
