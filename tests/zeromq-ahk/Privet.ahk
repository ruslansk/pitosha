; IMPORTANT INFO ABOUT GETTING STARTED: Lines that start with a
; semicolon, such as this one, are comments.  They are not executed.

; This script has a special filename and path because it is automatically
; launched when you run the program directly.  Also, any text file whose
; name ends in .ahk is associated with the program, which means that it
; can be launched simply by double-clicking it.  You can have as many .ahk
; files as you want, located in any folder.  You can also run more than
; one .ahk file simultaneously and each will get its own tray icon.

; SAMPLE HOTKEYS: Below are two sample hotkeys.  The first is Win+Z and it
; launches a web site in the default browser.  The second is Control+Alt+N
; and it launches a new Notepad window (or activates an existing one).  To
; try out these hotkeys, run AutoHotkey again, which will load this file.

;MyLabel:
;Clipboard = ; Буфер обмена пуст
;ClipWait,
;if ErrorLevel <> 0
;{
;	MsgBox, Попытка скопировать текст в буфер обмена неудачна.
;	Return
;}
;MsgBox, clipboard = %clipboard%
;;Clipboard = ; Буфер обмена пуст
;;Return
;Goto, MyLabel

NeedleNeedle = False 

OnClipboardChange:
{
  if NeedleNeedle = False
  {
      NeedleNeedle = True
	  return
  }
  if NeedleNeedle = True
  {
      NeedleNeedle = TrueTrue
	  return
  }

  Needle = AHK::Directum
  IfInString, clipboard, %Needle%
  {
      Gosub, GDirectum
      Clipboard =       ; Буфер обмена пуст
  }
  Needle = AHK::Persons
  IfInString, clipboard, %Needle%
  {
      Gosub, GPersons
      Clipboard =       ; Буфер обмена пуст
  }
}
return

GDirectum:
;MsgBox, Подпрограмма Directum
{
  if !winexist("ahk_class TSBLoginPromtByConfigInfoForm")  
  {  
    Run, "C:\Program Files\DIRECTUM Company\DIRECTUM 4.7\SBRte.exe" -CT=EdmsExplorer -SYS=DIRECTUM  
    WinWaitActive, ahk_class TSBLoginPromtByConfigInfoForm,, 2  
    if ErrorLevel  
      return  
  }  
  else if winexist("ahk_class TSBLoginPromtByConfigInfoForm") 
  {  
    WinActivate, ahk_class TSBLoginPromtByConfigInfoForm  
    WinWaitActive, ahk_class TSBLoginPromtByConfigInfoForm,, 2  
    if ErrorLevel
      return  
  }
  Send +{tab}tester+{tab}DIRECTUM+{tab}SQL-SERVER+{tab}+{tab}+{tab}QQQw21{enter}
}
return

GPersons:
;MsgBox, Подпрограмма Persons
{
  Run http://195.144.216.23:48080/persons_cntr/
  WinWaitActive, ahk_class #32770,, 2  
  if ErrorLevel  
    return
  Send import_usr{tab}import_usr{enter}
}
return
  
#w::
Run http://195.144.216.23:48080/persons_cntr/
WinWaitActive, ahk_class #32770,, 2  
if ErrorLevel  
    return
Send import_usr{tab}import_usr{enter}
return

; #space::
; Send Здрасти,{Enter}Добрый день!
; return

; #space::
; Send ^с!{tab}Вставить:^м
; return

#space::  
{  
  if !winexist("ahk_class MSPaintApp")  
  {  
    Run, mspaint.exe  
    WinWaitActive, ahk_class MSPaintApp,, 2  
    if ErrorLevel  
      return  
  }  
  else if winexist("ahk_class MSPaintApp") 
  {  
    WinActivate, ahk_class MSPaintApp  
    WinWaitActive, ahk_class MSPaintApp,, 2  
    if ErrorLevel
      return  
  }  
  MouseClickDrag, L, 150, 250, 150, 150  
  MouseClickDrag, L, 150, 150, 200, 100  
  MouseClickDrag, L, 200, 100, 250, 150  
  MouseClickDrag, L, 250, 150, 150, 150  
  MouseClickDrag, L, 150, 150, 250, 250  
  MouseClickDrag, L, 250, 250, 250, 150  
  MouseClickDrag, L, 250, 150, 150, 250  
  MouseClickDrag, L, 150, 250, 250, 250  
}  
return

#a::
{
  Run, mspaint.exe
  WinWaitActive, ahk_class MSPaintApp,, 2
  if ErrorLevel
    return
  MouseClickDrag, L, 150, 250, 150, 150
  MouseClickDrag, L, 150, 150, 200, 100
  MouseClickDrag, L, 200, 100, 250, 150
  MouseClickDrag, L, 250, 150, 150, 150
  MouseClickDrag, L, 150, 150, 250, 250
  MouseClickDrag, L, 250, 250, 250, 150
  MouseClickDrag, L, 250, 150, 150, 250
  MouseClickDrag, L, 150, 250, 250, 250
}
return

#q::
{
  if !winexist("ahk_class TSBLoginPromtByConfigInfoForm")  
  {  
    Run, "C:\Program Files\DIRECTUM Company\DIRECTUM 4.7\SBRte.exe" -CT=EdmsExplorer -SYS=DIRECTUM  
    WinWaitActive, ahk_class TSBLoginPromtByConfigInfoForm,, 2  
    if ErrorLevel  
      return  
  }  
  else if winexist("ahk_class TSBLoginPromtByConfigInfoForm") 
  {  
    WinActivate, ahk_class TSBLoginPromtByConfigInfoForm  
    WinWaitActive, ahk_class TSBLoginPromtByConfigInfoForm,, 2  
    if ErrorLevel
      return  
  }
  Send +{tab}tester+{tab}DIRECTUM+{tab}SQL-SERVER+{tab}+{tab}+{tab}QQQw21{enter}
}
return

; #space::Run www.gimp-master.moy.su

#z::Run www.autohotkey.com

^!n::
IfWinExist Untitled - Notepad
	WinActivate
else
	Run Notepad
return


; Note: From now on whenever you run AutoHotkey directly, this script
; will be loaded.  So feel free to customize it to suit your needs.

; Please read the QUICK-START TUTORIAL near the top of the help file.
; It explains how to perform common automation tasks such as sending
; keystrokes and mouse clicks.  It also explains more about hotkeys.
