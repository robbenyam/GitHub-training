set PATH=%PATH%;H:\bin

@cd /d %~dp0
@cd ..\15_chatter
echo �ڕW�f�[�^�̊J�n���F
set/P VAR_1=
echo �ڕW�f�[�^�̍Ō���F
set/P VAR_2=
python sf_connection.py %VAR_1% %VAR_2%