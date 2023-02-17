Attribute VB_Name = "NewMacros"
Sub SelectXMLMarkup()
'
' SelectXMLMarkup Макрос
'
'
' Value = InputBox("name: ")
' MsgBox (ActiveDocument.Paragraphs(1).Range.Text)
Dim Paragraph As Word.Paragraph
Dim StartTag As String
Dim EndTag As String

If Selection.Type = wdSelectionNormal Then
    TagName = InputBox("Name")
    If TagName <> "" Then
        StartTag = "{{" & TagName & "|"
        EndTag = "}}"
        Selection.InsertBefore (StartTag)
        Selection.InsertAfter (EndTag)
        ActiveDocument.Range(Selection.Start, Selection.Start + Len(StartTag)).Style = "xml-markup"
        ActiveDocument.Range(Selection.End - Len(EndTag), Selection.End).Style = "xml-markup"
    End If
End If

End Sub
