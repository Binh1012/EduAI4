package com.eduai4.app

import android.app.Application
import com.eduai4.app.data.Graph

class EduApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Graph.init(this)
    }
}
