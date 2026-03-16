# WebView app – keep Activity and WebView callbacks
-keep class com.hydroportable.app.** { *; }
-keepclassmembers class * extends android.webkit.WebViewClient { *; }
