set PATH=%PATH%;H:\bin

@cd /d %~dp0
@cd ..\15_chatter
echo 目標データの開始日：
set/P VAR_1=
echo 目標データの最後日：
set/P VAR_2=
python sf_connection.py %VAR_1% %VAR_2%