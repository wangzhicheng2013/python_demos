#!/bin/sh

BASEPATH=$(cd `dirname $0`;pwd)
PACKNAME=`ls "$BASEPATH"|grep -e "mongodb.*\.tgz"|awk -F ".tgz" '{print $1}'`

OUTPUT=$BASEPATH/start.out
TGZ=$BASEPATH/$PACKNAME.tgz
DIR=$BASEPATH/$PACKNAME


if [ -z "`sed -n '/^mongod:/p' /etc/group`" ];then
	groupadd mongod
	echo "add group mongod"
fi

if [ -z "`sed -n '/^mongod:/p' /etc/passwd`" ];then
	rm -rf /var/spool/mail/mongod >/dev/null 2>&1
	rm -rf "$BASEPATH/mongod" >/dev/null 2>&1
	useradd -g mongod -d "$BASEPATH"/mongod mongod
	echo "add user mongod to group 'mongod'"
fi

DATADIR=$BASEPATH/data
if [ ! -d $DATADIR ];then
	mkdir -p $DATADIR
	chown mongod:mongod $DATADIR
fi

#解压
if [ -f $TGZ -a ! -d $DIR ];then
	mkdir $DIR
	tar -zxvf $TGZ -C $BASEPATH
fi



MONGOD=`find $BASEPATH -path "*/bin/mongod"`
MONGO=`find $BASEPATH -path "*/bin/mongo"`
#CONF=`find $BASEPATH -name "mongod_fork.conf"`
CONF=$BASEPATH/mongod.conf

if [ -z "$CONF" ];then
    echo "missing mongod.conf"
elif [ -z "$MONGOD" ];then
    echo "missing mongod"
fi

#根据/opt/vulscan/etc/settings.properties获取ipv6的信息
IFS="="

isIpv6=false
while read k v
do
  if [ "$k" == "isIpv6" ];then
   isIpv6=$v
   break;
  fi
done < /opt/vulscan/etc/settings.properties

#授权
if [ $isIpv6 == "true" ];then
   echo "begin ipv6 auth"
   $MONGOD --ipv6 -f $CONF > $OUTPUT 2>&1 &
else
   echo "begin ipv4 auth"
   $MONGOD -f $CONF > $OUTPUT 2>&1 &
fi

#mongo授权是否成功的标志，1代表失败，0代表成功
mongo_auth_reult=1
for((i=1;i<=3;i++));
do
	if [ -z "`netstat -ntpl|grep 27017`" ];then
		echo 'waiting mongod be ready'
		sleep 5
	else
		echo 'mongod has been started,then authorize with root.'
		sleep 5
		for((j=1;j<=3;j++));
		do
		    if [ $isIpv6 == "true" ];then
		        echo "begin ipv6 set password"
		        $MONGO --ipv6 --host [::1] --port 27017 admin --eval "db.createUser({user:'root',pwd:'1qazCDE#5tgb',roles:[{role:'__system',db:'admin'}]})"
		    else
		        echo "begin ipv4 set password"
		        $MONGO admin --eval "db.createUser({user:'root',pwd:'1qazCDE#5tgb',roles:[{role:'__system',db:'admin'}]})"
		    fi
			if [ 0 == $? ];then
			    mongo_auth_reult=0
				echo 'authorized successfully'
				break;
			fi
			sleep 5
		done
		sleep 5
		break;
        fi
done

echo "mongo_auth_reult>>${mongo_auth_reult}"
exit ${mongo_auth_reult}
