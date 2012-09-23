set path="C:\Program Files (x86)\Vim\vim73\gvim.exe";%path%
C:\Python32\python.exe cleanup_html.py vivekananda vivekananda_1 
del vivekananda_1\complete_works.htm
del vivekananda_1\complete_works_contents.htm
copy backup\complete_works.htm vivekananda_1\complete_works.htm
copy backup\*.jpg vivekananda_1\
copy backup\complete_works_v1_contents.htm vivekananda_1\volume_1\complete_works_v1_contents.htm /Y
copy backup\volume_2_contents.htm vivekananda_1\volume_2\volume_2_contents.htm /Y
copy backup\volume_3_contents.htm vivekananda_1\volume_3\volume_3_contents.htm /Y
copy backup\volume_4_contents.htm vivekananda_1\volume_4\volume_4_contents.htm /Y
copy backup\volume_5_contents.htm vivekananda_1\volume_5\volume_5_contents.htm /Y
copy backup\volume_6_contents.htm vivekananda_1\volume_6\volume_6_contents.htm /Y
copy backup\volume_7_contents.htm vivekananda_1\volume_7\volume_7_contents.htm /Y
copy backup\volume_8_contents.htm vivekananda_1\volume_8\volume_8_contents.htm /Y
copy backup\volume_9_contents.htm vivekananda_1\volume_9\volume_9_contents.htm /Y
copy backup\appendices_contents.htm vivekananda_1\appendices\appendices_contents.htm /Y

echo removing Orphaned Files: 

del vivekananda_1\appendices\appendices.htm
del vivekananda_1\unpublished\unpublished.htm
del vivekananda_1\volume_4\writings_prose\reply_to_the_madras_address_2.htm
del vivekananda_1\volume_4\writings_prose\reply_to_the_madras_address_4.htm
del vivekananda_1\volume_4\writings_prose\reply_to_the_madras_address_6.htm
del vivekananda_1\volume_6\epistles_second_series\clarification.htm
del vivekananda_1\volume_6\epistles_second_series\pramadadas_mitra.htm

