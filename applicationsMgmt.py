#!/usr/bin/env python

"""applicationsMgmt.py: CLI for Applications Management BE-TEA Operations."""

import sys
import io
import os.path
import argparse
import tibco.tea
from utils import *

# Create the command-line ArgumentParser
def createCommandParser():
	#create the top-level parser
	commandParser = argparse.ArgumentParser(add_help = False, description = 'Applications Management Operations CLI.')
	commandParser.add_argument('-ssl', required = False, default = False, dest = 'sslEnabled', help = 'SSL Enabled')
	args = commandParser.parse_known_args()[0]
	commandParser.add_argument('-t', required = False, default = getDefaultTEAServerURL(args.sslEnabled), dest = 'serverURL', help = 'TEA Server URL')
	commandParser.add_argument('-u', required = True, dest = 'userName', help = 'TEA User Name')
	commandParser.add_argument('-p', required = True, dest = 'userPwd', help = 'TEA User Password')
	commandParser.add_argument('-sc', required = False, default = '', dest = 'serverCert', help = 'Server certificate Path')
	commandParser.add_argument('-cc', required = False, default = '', dest = 'clientCert', help = 'Client certificate Path')
	subparsers = commandParser.add_subparsers(dest='operationName')
	
	subparsersList = []
	for operation in operationsList:
		if (operation == 'addmachine'):
			addMachineParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			addMachineParser.add_argument('-m', required = True, dest = 'machineName', help = 'Machine name')
			addMachineParser.add_argument('-i', required = True, dest = 'ipAddress', help = 'Ip Address')
			addMachineParser.add_argument('-o', required = True, dest = 'OS', help = 'OS', choices=['windows', 'unix' , 'os-x'])
			addMachineParser.add_argument('-b', required = True, dest = 'beHome', help = 'BE Home')
			addMachineParser.add_argument('-t', required = True, dest = 'beTra', help = 'BE Home TRA file')
			addMachineParser.add_argument('-u', required = True, dest = 'user', help = 'Machine User')
			addMachineParser.add_argument('-p', required = True, dest = 'pwd', help = 'Machine User password')
			addMachineParser.add_argument('-s', required = True, dest = 'sshPort', help = 'SSH port')
			addMachineParser.add_argument('-f', required = True, dest = 'deploymentPath', help = 'Default Deployment Path')
			addMachineParser.set_defaults(func = addMachine)
			subparsersList.append(addMachineParser)
		elif (operation == 'createdeployment'):
			createDeploymentParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			createDeploymentParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			createDeploymentParser.add_argument('-c', required = True, dest = 'cddFile', help = 'CDD file')
			createDeploymentParser.add_argument('-e', required = True, dest = 'earFile', help = 'EAR file')
			createDeploymentParser.set_defaults(func = createDeployment)
			subparsersList.append(createDeploymentParser)
		elif (operation == 'importdeployment'):	
			importDeploymentParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			importDeploymentParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			importDeploymentParser.add_argument('-c', required = True, dest = 'cddFile', help = 'CDD file')
			importDeploymentParser.add_argument('-e', required = True, dest = 'earFile', help = 'EAR file')
			importDeploymentParser.add_argument('-s', required = True, dest = 'stFile', help = 'ST file')
			importDeploymentParser.set_defaults(func = importDeployment)
			subparsersList.append(importDeploymentParser)
		elif (operation == 'deletedeployment'):
			deleteDeploymentParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			deleteDeploymentParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			deleteDeploymentParser.set_defaults(func = deleteDeployment)
			subparsersList.append(deleteDeploymentParser)			
		elif (operation == 'createinstance'):
			createInstanceParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			createInstanceParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			createInstanceParser.add_argument('-i', required = True, dest = 'instanceName', help = 'Instance name')
			createInstanceParser.add_argument('-u', required = True, dest = 'pu', help = 'Processing Unit')
			createInstanceParser.add_argument('-m', required = True, dest = 'machineName', help = 'Machine name')
			createInstanceParser.add_argument('-p', required = True, dest = 'jmxPort', help = 'JMX Port')
			createInstanceParser.add_argument('-f', required = False, dest = 'deploymentPath', help = 'Deployment Path')
			createInstanceParser.add_argument('-ju', required = False, dest = 'jmxuser', help = 'JMX User Name')
			createInstanceParser.add_argument('-jp', required = False, dest = 'jmxpass', help = 'JMX Password')
			createInstanceParser.set_defaults(func = createInstance)
			subparsersList.append(createInstanceParser)
		elif (operation == 'copyinstance'):
			copyInstanceParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			copyInstanceParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			copyInstanceParser.add_argument('-i', required = True, dest = 'instanceName', help = 'Instance to copy')
			copyInstanceParser.add_argument('-n', required = True, dest = 'newInstanceName', help = 'New Instance name')
			copyInstanceParser.add_argument('-u', required = True, dest = 'pu', help = 'Processing Unit')
			copyInstanceParser.add_argument('-m', required = True, dest = 'machineName', help = 'Machine name')
			copyInstanceParser.add_argument('-p', required = True, dest = 'jmxPort', help = 'JMX Port')
			copyInstanceParser.add_argument('-f', required = True, dest = 'deploymentPath', help = 'Deployment Path')
			copyInstanceParser.add_argument('-ju', required = False, dest = 'jmxuser', help = 'JMX User Name')
			copyInstanceParser.add_argument('-jp', required = False, dest = 'jmxpass', help = 'JMX Password')
			copyInstanceParser.set_defaults(func = copyInstance)
			subparsersList.append(copyInstanceParser)
		elif (operation == 'deleteinstance'):
			deleteInstanceParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			deleteInstanceParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			deleteInstanceParser.add_argument('-i', required = True, dest = 'instanceName', help = 'Instance name')
			deleteInstanceParser.set_defaults(func = deleteInstance)
			subparsersList.append(deleteInstanceParser)
		elif operation in ['deploy', 'undeploy', 'start', 'stop']:
			mgmtOprParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			mgmtOprParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			group = mgmtOprParser.add_mutually_exclusive_group()
			group.add_argument('-m', required = False, dest = 'machine', help = 'Machine name')
			group.add_argument('-u', required = False, dest = 'pu', help = 'Processing Unit')
			group.add_argument('-a', required = False, dest = 'agentClass', help = 'BE Agent class')
			mgmtOprParser.add_argument('-i', nargs='*', dest = 'instances', help = 'List of instance names')	
			mgmtOprParser.set_defaults(func = invokeMgmtOperation)
			subparsersList.append(mgmtOprParser)
		elif (operation == 'hotdeploy'):
			#hot-deploy argument parser
			hotdeployParser = subparsers.add_parser(operation, prog = operation, add_help = False)
			hotdeployParser.add_argument('-d', required = True, dest = 'applicationName', help = 'Application deployment name')
			hotdeployParser.add_argument('-e', required = True, dest = 'earFile', help = 'Deployment EAR file')
			hotdeployParser.set_defaults(func = hotdeploy)
			subparsersList.append(hotdeployParser)

	return commandParser, subparsersList

##########################################################################################################################################
# Application Management operations
##########################################################################################################################################
# Add Machine operation
def addMachine (args):
	try:
		print('Executing operation - addmachine')
		OS = args.OS
		if(OS == "windows"):
			OS = "Windows Based"
		else:
			OS = "OS/X,Unix/Linux Based"
		result = beProduct.addMasterHost(args.machineName, args.ipAddress, OS, args.beHome, args.beTra, args.user, args.pwd, args.sshPort, args.deploymentPath)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# Create Deployment operation
def createDeployment(args):
	cddFileHandle = None
	earFileHandle = None
	try:
		print('Executing operation - createdeployment')
		if (os.path.isfile(args.cddFile)):
			if (not os.access(args.cddFile, os.R_OK)):
				print('Cannot read CDD file ' + args.cddFile)
				exit()
		else:
			print('CDD file ' + args.cddFile + ' not found')
			exit()
		if (os.path.isfile(args.earFile)):
			if (not os.access(args.earFile, os.R_OK)):
				print('Cannot read EAR file ' + args.earFile)
				exit()
		else:
			print('EAR file ' + args.earFile + ' not found')
			exit()
					
		cddFileHandle = io.open(args.cddFile, 'rb')
		earFileHandle = io.open(args.earFile, 'rb')
		with tea.timeout(30):
			result = beProduct.upload(args.applicationName, '', cddFileHandle, earFileHandle, '', True)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)
	finally:
		if (cddFileHandle):
			cddFileHandle.close()
		if (earFileHandle):
			earFileHandle.close()

# Import Deployment operation
def importDeployment(args):
	cddFileHandle = None
	earFileHandle = None
	stFileHandle = None
	try:
		print('Executing operation - importdeployment')
		if (os.path.isfile(args.cddFile)):
			if (not os.access(args.cddFile, os.R_OK)):
				print('Cannot read CDD file ' + args.cddFile)
				exit()
		else:
			print('CDD file ' + args.cddFile + ' not found')
			exit()
		if (os.path.isfile(args.earFile)):
			if (not os.access(args.earFile, os.R_OK)):
				print('Cannot read EAR file ' + args.earFile)
				exit()
		else:
			print('EAR file ' + args.earFile + ' not found')
			exit()
		if (os.path.isfile(args.stFile)):
			if (not os.access(args.stFile, os.R_OK)):
				print('Cannot read Site Topology file ' + args.stFile)
				exit()
		else:
			print('Site Topology file ' + args.stFile + ' not found')
			exit()
		cddFileHandle = io.open(args.cddFile, 'rb')
		earFileHandle = io.open(args.earFile, 'rb')
		stFileHandle = io.open(args.stFile, 'rb')
		with tea.timeout(30):
			result = beProduct.upload(args.applicationName, '', cddFileHandle, earFileHandle, stFileHandle, False)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)
	finally:
		if (cddFileHandle):
			cddFileHandle.close()
		if (earFileHandle):
			earFileHandle.close()

# Delete Deployment operation
def deleteDeployment(args):
	try:
		print ('Executing operation - deletedeployment')
		beApplication = getApplication(beProduct, args.applicationName)		
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			exit()
		with tea.timeout(30):
			result = beApplication.delete()
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# Create Instance operation
def createInstance(args):
	try:
		print ('Executing operation - createinstance')
		beApplication = getApplication(beProduct, args.applicationName)		
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			exit()
		result = beApplication.createServiceInstance(args.instanceName, args.pu, args.machineName, args.jmxPort, args.deploymentPath, args.jmxuser, args.jmxpass)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# Copy Instance operation
def copyInstance(args):
	try:
		print ('Executing operation - copyinstance')
		beApplication = getApplication(beProduct, args.applicationName)
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			exit()
		beServiceInstance = getServiceInstance(beApplication, args.instanceName)
		if (not beServiceInstance):
			print('Instance ' + args.instanceName + ' not found')
			exit()
		result = beServiceInstance.copyInstance(args.newInstanceName, args.pu, args.machineName, args.jmxPort, args.deploymentPath, args.jmxuser, args.jmxpass)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# Delete Instance operation
def deleteInstance(args):
	try:
		print ('Executing operation - deleteinstance')
		beApplication = getApplication(beProduct, args.applicationName)
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			exit()
		beServiceInstance = getServiceInstance(beApplication, args.instanceName)
		if (not beServiceInstance):
			print('Instance ' + args.instanceName + ' not found')
			exit()
		result = beServiceInstance.delete()
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# deploy/undeploy/start/stop instance(s) operations
def invokeMgmtOperation (args):
	try:
		teaObjectType = None
		print ('Executing operation - ' + args.operationName)
		beApplication = getApplication(beProduct, args.applicationName)
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			print('Exiting...')
			exit()
		if (args.machine):
			teaObjectType = 'Machine'
			beTeaObject = getApplicationHost(beApplication, args.machine)
		elif (args.pu):
			teaObjectType = 'PU'
			beTeaObject = getApplicationPU(beApplication, args.pu)
		elif (args.agentClass):
			teaObjectType = 'AgentClass'
			beTeaObject = getApplicationPuAgent(beApplication, args.agentClass)
		else:
			teaObjectType = 'Application'
			beTeaObject = beApplication
		
		instanceKeys = []
		if (args.instances and len(args.instances) > 0):
			for instanceName in args.instances:
				serviceInstance = getServiceInstance(beTeaObject, instanceName)
				if (serviceInstance):
					instanceKeys.append(serviceInstance.key)
				else:
					print('Instance ' + instanceName + ' not found for ' + teaObjectType + ' ' + beTeaObject.name)
			with tea.timeout(30):
				result = getattr(beTeaObject, args.operationName)(instanceKeys)	
			print(result)
		else:
			for serviceInstance in beTeaObject.ServiceInstances.values():
				instanceKeys.append(serviceInstance.key)
			with tea.timeout(30):
				result = getattr(beTeaObject, args.operationName)(instanceKeys)		
			print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)

# Application Deployment hotdeploy operation
def hotdeploy (args):
	fileHandle = None
	try:
		print ('Executing operation - hotdeploy')
		beApplication = getApplication(beProduct, args.applicationName)		
		if (not beApplication):
			print('Application ' + args.applicationName + ' not found')
			exit()
		if (os.path.isfile(args.earFile)):
			if (not os.access(args.earFile, os.R_OK)):
				print('Cannot read EAR file ' + args.earFile)
				exit()
		else:
			print('EAR file ' + args.earFile + ' not found')
			print('Exiting...')
			exit()
					
		fileHandle = io.open(args.earFile, 'rb')
		with tea.timeout(30):
			result = beApplication.hotdeployAll(fileHandle)
		print(result)
	except Exception as ex:
		details = ex.args[0]
		print(details)
	finally:
		if (fileHandle):
			fileHandle.close()

##########################################################################################################################################
# Startup code
##########################################################################################################################################
operationsList = ['deploy', 'undeploy', 'start', 'stop', 'hotdeploy', 'addmachine', 'createdeployment', 'importdeployment', 'createinstance', 'copyinstance', 'deleteinstance', 'deletedeployment']			
# Create Command parser
commamdParser, subparsersList = createCommandParser()
if (len(sys.argv) == 1): # Print complete usage & exit
	printCompleteUsage(commamdParser, subparsersList)
	exit()
#Parse the command arguments
command = commamdParser.parse_args()
if (command.operationName): #Execute operation
	tea = connectToServer(command.serverURL, command.userName, command.userPwd, command.sslEnabled, command.serverCert, command.clientCert)
	beProduct = tea.products['BusinessEvents']
	if (beProduct.status == 'Running'): # BE TEA Agent is not running
		command.func(command)
	else:
		print('TEA Server returned - '+ beProduct.__name__ + ' TEA Agent not reachable')
		exit()
else: #Print operation usage
	commamdParser.print_usage()
	print('Exiting...')
	exit()
