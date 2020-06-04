#!/bin/bash

#cp ../../Certificates/* ./
echo "Copying certificates from /home.pi/Certificates to Certificates directory"

cp /home/pi/Certificates/*.pem.crt /home/pi/CS179J-Team01/Certificates/device-certificate.pem.crt
cp /home/pi/Certificates/*private.pem.key /home/pi/CS179J-Team01/Certificates/device-private.pem.key
cp /home/pi/Certificates/*public.pem.key /home/pi/CS179J-Team01/Certificates/device-public.pem.key
cp /home/pi/Certificates/*CA.crt /home/pi/CS179J-Team01/Certificates/root-CA.crt

if [ "$?" = "0" ]; then
	echo "Copy Successful"
else
  echo "Something went wrong"
	exit 1
fi

exit 1
