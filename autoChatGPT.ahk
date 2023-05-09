
; 接受入参
if A_Args.Length >= 1 {
    A_Clipboard := ""
    askText := ""
    for argText in A_Args {
        askText := askText " " argText
    }
}
else {
    MsgBox "没有入参"
    A_Clipboard := ""
    ExitApp
}

; 获取显示器尺寸
try {
    MonitorGet 1, &Left, &Top, &Right, &Bottom
    windowWidth := Right
    windowHeight := Bottom
}
catch {
    MsgBox "未获取到正确的屏幕尺寸"
    A_Clipboard := ""
    ExitApp
}

; 打开浏览器
; if WinExist("ahk_exe firefox.exe") {
if WinExist("ahk_exe msedge.exe") {
    WinActivate     ; 激活窗口
    WinMaximize     ; 最大化
    Sleep 200
}
else{
    MsgBox "Firefox 浏览器未启动，请启动浏览器并登录chatGPT。"
    A_Clipboard := ""
    ExitApp
}

CoordMode "Pixel"  ; 将下面的坐标解释为相对于屏幕而不是活动窗口.

; 打开ChatGPT页面 找Logo颜色，只找一个点
if PixelSearch(&Px, &Py, 0, 0, windowWidth, 60, 0x75a99c, 3) {
    MouseClick "left", Px+20, Py+10
    Sleep 2000
}
else {
    MsgBox "未发现 ChatGPT 页面图标颜色，检查ChatGPT页面是否打开"
    A_Clipboard := ""
    ExitApp
}


; 开油猴脚本，找黄色 textbox
if PixelSearch(&Px, &Py,windowWidth/2, Bottom/2, windowWidth, Bottom, 0xffff00, 0) {    ; 从右下方找
    MouseClick "left", Px+20, Py+10
    Sleep 200
    A_Clipboard := askText
    Send "^a"
    Send "{del}"
    Send "^v"
    Sleep 200
    Send "{Enter}"
    Sleep 10000
}
else{
    MsgBox "未发现 send a message 文本框"
    A_Clipboard := ""
    ExitApp
}

; 180秒等待结果
resultFlag := 0
Loop 180 {
    ; 开油猴脚本，找红色 copy button
    if PixelSearch(&Px, &Py,windowWidth-50, 0, windowWidth, Bottom/2, 0xff0000, 0) {    ; 从右上方找
        A_Clipboard := ""
        Sleep 1000
        MouseClick "left", Px+20, Py+10
        ClipWait
        WinMinimize
        Sleep 500
        ExitApp
    }

    ; 监测网络断掉 重发
    if PixelSearch(&Px, &Py,windowWidth/2, Bottom/2, windowWidth, Bottom, 0x10a37f, 3) {    ; 从右下方找
        MouseClick "left", Px+20, Py+10
    }

    Sleep 1000
}

MsgBox "超时，请检查原因"
A_Clipboard := ""
ExitApp
