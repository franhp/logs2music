#!/usr/bin/env python
import sys, random, time

MESSAGES = [
'[] INFO 2013-05-02 10:48:51,934 e.t.g.s.i.AccountService Invoking method [AccountService.findUserByNickname()] with parameters [napaman, false]',
'[] ERROR 2013-04-22 12:14:12,447 e.t.g.h.RestClient3 Call to resource [http://localhost:8080/goldengate/protected/users/tethering/updateproductid] with parameters [{user_id=23699, order_id=248741}] returned status code [500]',
'[] WARN 2013-04-19 15:30:46,997 o.j.j.x.JpdlXmlReader process parse warning: swimlane \'admin\' does not have an assignment',
'[] ERROR 2013-04-22 12:14:12,448 e.t.g.j.t.ChangeFupProductId BPM threw exception in Process Definition [TopUp]. Node [Change FUP Product ID] has thrown exception: es.tid.gg.http.exception.HttpResponseException: {"_meta":{"type":"ERROR"},"_payload":null}',
'[] INFO 2013-04-22 10:28:52,842 o.h.i.SessionFactoryObjectFactory Not binding factory to JNDI, no JNDI name configured',
'[] INFO 2013-04-22 10:28:51,009 o.h.cfg.HbmBinder Mapping collection: org.jbpm.graph.action.Script.variableAccesses -> JBPM_VARIABLEACCESS',
'[] INFO 2013-04-19 16:42:46,700 o.h.c.SettingsFactory JPA-QL strict compliance: disabled',
'[] INFO 2013-04-19 16:42:46,537 o.h.cfg.HbmBinder Mapping subclass: org.jbpm.taskmgmt.log.TaskCreateLog -> JBPM_LOG',
]

if len(sys.argv) < 2:
	sys.exit('Usage: python %s filename.log'%sys.argv[0])

while True:
	with open(sys.argv[1],'ab') as f:
		f.write(MESSAGES[random.randint(0,len(MESSAGES)-1)] + '\n')
		time.sleep(0.5)
	f.close()