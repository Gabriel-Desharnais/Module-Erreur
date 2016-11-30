#! /usr/bin/python3
# coding: utf8

""" Ce module permet de calculer num|é|riquement l'incertitude
    d'une fonction par rapport |à| l'incertitude de ces param|è|tres
    En th|é|orie |ç|a marche, mais aucune garantie.
    (c)Gabriel Desharnais, 2016. Fa|î|tes-en ce que vous-voulez."""
    
import numpy as np
from scipy import misc

def result(n,e):            #fonction de formatage de sortie
	ordre = int(np.floor(np.log10(e)))
	if ordre < 0 :
		f = "{:."+str(-ordre)+"f}"
		re = f.format(n)
	else:
		#|à| changer
		re=str(n)
	return re
	
def resultI(n,e):
	ordre = int(np.floor(np.log10(e)))
	re = np.around(n,-ordre)
	return re
def rotate(l,n):            #fonction pour rotater une liste
	return l[n:]+l[:n]

def wrap(*ag):              #fonction interfa|ç|ant la vrai fonction
	global n
	global M
	return M(*rotate(ag,-n))

def err(f,ar,e):
	t=0
	global n
	n=0
	for x in range(len(ar)):
		ar=rotate(ar,1)
		t+=np.abs(misc.derivative(f,ar[0],args=ar[:-1])*e[x])
		n+=1
	return t

def erreur(fonction,arguments,erreurs):
	global M
	M=fonction
	return err(wrap,arguments,erreurs)
def error(func):
	def supper(*args,**ag):
		try:
			return erreur(func,args,ag['er'])
		except KeyError:
			return func(*args)
	return supper

def e(func):
	def supper(*args,**ag):
		try:
			return resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er']))
		except KeyError:
			return func(*args)
	return supper

def es(func):
	def supper(*args,**ag):
		try:
			return str( resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er'])))
		except KeyError:
			return func(*args)
	return supper
def rs(func):
	def supper(*args,**ag):
		try:
			return str( resultI(func(*args),erreur(func,args,ag['er'])))+'±'+str( resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er'])))
		except KeyError:
			return func(*args)
	return supper

def rl(func):
	def supper(*args,**ag):
		try:
			return [ resultI(func(*args),erreur(func,args,ag['er'])), resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er']))]
		except KeyError:
			return func(*args)
	return supper

def rls(func):
	def supper(*args,**ag):
		try:
			return [str( resultI(func(*args),erreur(func,args,ag['er']))),str( resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er'])))]
		except KeyError:
			return func(*args)
	return supper

def resultatl(func):
	def supper(*args,**ag):
		try:
			return [func(*args),erreur(func,args,ag['er'])]
		except KeyError:
			return func(*args)
	return supper
def rst(func):
	def supper(*args,**ag):
		try:
			return '$'+str( resultI(func(*args),erreur(func,args,ag['er'])))+'\pm'+str( resultI(erreur(func,args,ag['er']),erreur(func,args,ag['er'])))+'$'
		except KeyError:
			return func(*args)
	return supper
n=0
M=0