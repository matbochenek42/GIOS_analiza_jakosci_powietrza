```
Sub Wyczysc_Fragmentatory()

    Dim wb As Workbook
    Dim sc As SlicerCache

    Set wb = ActiveWorkbook

    Application.ScreenUpdating = False
    Application.EnableEvents = False
    ' wyłączenie odświeżenia ekranu i działań (żeby makro działało)
    
    ' pętla po wszystkich fragmentatorach
    For Each sc In wb.SlicerCaches
        
        sc.ClearAllFilters ' wyczyść fragmentator

    Next sc

    Application.EnableEvents = True
    Application.ScreenUpdating = True


    MsgBox "Wyczyszczono wszystkie filtry fragmentatorów i osi czasu."

End Sub
```