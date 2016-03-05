#!/bin/sh
#--------------------------------------------------------------------------
# set platform
#     set_platform.sh xxxx	
#           set platform for xxxx customer
#     set_platform.sh 0
#           clear platform setting
#--------------------------------------------------------------------------

CUR_DIR=$PWD

#sowell config flag.
if [ $1 == "ott-sample" ] || [ $1 == "dvb-sample" ] ; then
	SOWELL_ANDROID_CONFIG_NAME=sw01
#else
#	SOWELL_ANDROID_CONFIG_NAME=htv
fi
#SOWELL_CUSTOMER_NAME=unknow
#SOWELL_CONFIG_FLAG=false

#define some dir
DIR_PRODUCT_OUTPUT=${CUR_DIR}/out/target/product/${SOWELL_ANDROID_CONFIG_NAME}
DIR_SPI_TOOL=${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/spi_tools
DIR_KERNEL_ROOT={CUR_DIR}/common/
DIR_KEY=${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/keystore

#factory mode for factory product
unset SOWELL_FACTORY_MODE
SOWELL_FACTORY_MODE=false

#function define
NO_DVB=true
NO_FTV=true
NO_OSCAM=true
NO_HTV=true

#define app and bins
APPS="Test SwlDvb SwlFtv SwlTvOnline SwlNetVideos SwlLauncher2 SwlUserManual SwlMyAPP SwlUpdate SwlVideoSearch SwlNetNavigation SwlMarket2 AuthService RemoteServer"
LIBS="jnidvbclientsubtitle2 forcetv SwlJni sw_adp"
BINS="HelloWorld snTarget"
HTV_PREBUILT_APPS="CxTvMarket CxTvSettings HtvLauncher HtvWelcome"

show-usage()
{
	echo  "mx build usage : "
	echo  "source sowell-setup.sh <customer> <factory>"
	echo  "    \"customer = XXXX\" set customer name"
    echo  "    \"customer = ott-sample \"          iptv sample, lauguage is english"
	echo  "    \"customer = dvb-sample \"          dvb sample, lauguage is english"
	echo  "    \"factory \"     	build for factory mode."
	echo  ""
	echo  "mk-uboot :     		build uboot "
	echo  "mk-spi-bin :     	build spi bin "
	echo  "mk-kernel: 		build  kernel"
	echo  "mk-recovery:		build  recovery"
	echo  "mk-otapackage: 		build  otapackage"
	echo  "mk-customer-package: 	build customer's otapackage as your config"
}

delete_svn_dir()
{
	echo "Rm -rf docs .svn"
	cd $CUR_DIR/framework/base/docs/
	pwd
	find . -type d -name ".svn"|xargs rm -rf
	croot
}

setup-config()
{
	echo "setup config start..."
	echo  "build/envsetup.sh ..."
	source  build/envsetup.sh
	echo  "lunch ${SOWELL_ANDROID_CONFIG_NAME}-user ..."
#	lunch   ${SOWELL_ANDROID_CONFIG_NAME}-user
	lunch  sw01-user 
#	lunch   ${SOWELL_ANDROID_CONFIG_NAME}-eng
	
	echo  "PATH, add build tools "
	echo  ""

	SOWELL_CONFIG_FLAG=true	

	echo "setup config end..."
}

extractJniLib()
{
	echo -e "\033[0;35m ===================ExtractJnilib START=======================\033[0m"
	echo -e "\033[0;35m ExtractJnilib from  prebuilt apk\033[0m"
	cd ${CUR_DIR}/vendor/sowell/prebuilt
	rm -rf extractedJniLibs/*.so
	./extractJniLib.sh SwlFtv.apk
	./extractJniLib.sh RemoteServer.apk
	du -h extractedJniLibs/*.so
	cp extractedJniLibs/*.so ${DIR_SOWELL_OUTPUT}/system/lib/
	cd ${CUR_DIR}
	echo -e "\033[0;35m ExtractJnilib from  prebuilt apk\033[0m"
	echo -e "\033[0;35m ===================ExtractJnilib END=========================\033[0m"
}

mk-root()
{
	echo "make root start..."

	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then

		for i in $BINS; do
			rm -rf $ANDROID_BUILD_TOP/out/target/product/$TARGET_PRODUCT/obj/EXECUTABLES/$i_intermediates
		done

		for i in $APPS; do
			rm -rf $ANDROID_BUILD_TOP/out/target/product/$TARGET_PRODUCT/obj/APPS/$i_intermediates
		done

		cd ${CUR_DIR}
		make -j8

        echo -e "\033[0;35m Build Sowell app or bin\033[0m"
		touch ${CUR_DIR}/packages/sowell/code/swlpackage/Helloworld/Common/sw_config.cpp
		touch ${CUR_DIR}/packages/sowell/code/swlpackage/Helloworld/HelloWorld.cpp
        cd ${CUR_DIR}/packages/sowell/
        mm -j8
        cd ${CUR_DIR}

	else 
		echo -e "\033[1;40;31m"not setup config"\033[0m\n"
	fi

	echo "make root end..."
}

mk-kernel()
{
	echo "make kernel start ..."

	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then
		cd ${CUR_DIR}
#device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/quick_build_kernel.sh bootimage meson6_s01_jbmr1_defconfig
		device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/quick_build_kernel.sh bootimage
		#??here need check, cp ${CUR_DIR}/common/arch/arm/boot/uImage ${DIR_SPI_TOOL}/uImage
	else 
		echo -e "\033[1;40;31m"not setup config"\033[0m\n"
	fi

	echo "make kernel end ..."
}

mk-recovery()
{
	echo "make recovery  start ..."

	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then 
		cd ${CUR_DIR}
		#./device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/quick_build_kernel.sh recoveryimage meson6_s01_recovery_defconfig
		./device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/quick_build_kernel.sh recoveryimage 
		#meson6_s01_recovery_defconfig
		#??here need check, cp ${CUR_DIR}/common/arch/arm/boot/uImage ${DIR_SPI_TOOL}/uImage_recovery
	else 
		echo -e "\033[1;40;31m"not setup config"\033[0m\n"
	fi

	echo "make recovery end .. " 
}

mk-uboot()
{
	echo "make uboot start ... "	
	make_uboot_ret=-1
	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then 
		cd ${CUR_DIR}/uboot 
#cd ${CUR_DIR}/uboot_skynoon
		make m8b_m201_1G_config
		make clean
		make && make_uboot_ret=$?
		cd ${CUR_DIR}
	else
		echo -e "\033[1;40;31m"not setup config"\033[0m\n"
	fi	
	
	if [ "${make_uboot_ret}" = "0" ];then
		echo "make uboot success"
	else
		echo -e "\033[1;40;31m"make uboot fail"\033[0m\n"
	fi

	echo "make uboot end ... "
}

#mk-spi-bin()
#{
#	echo "mk-spi-bin start ..."
#	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then 
#		cp ${CUR_DIR}/uboot/build/u-boot.bin  ${DIR_SPI_TOOL}
#
#		cd ${DIR_SPI_TOOL}
#		chmod +x makespi4m_m3.sh
#       ./makespi4m_m3.sh u-boot.bin defaultargs.txt uImage_recovery
#		cp spi.bin ${DIR_PRODUCT_OUTPUT}/spi.bin
#		if [  -f ${DIR_PRODUCT_OUTPUT}/spi.bin ]; then
#			cp  ${DIR_PRODUCT_OUTPUT}/spi.bin ${DIR_PRODUCT_OUTPUT}/spi-${SOWELL_CUSTOMER_NAME}.bin
#			echo "copy spi.bin..."
#		fi
#		cd ${CUR_DIR}
#	fi	
#	echo "mk-spi-bin end..."
#}
		
check-customer-apk()
{
	echo "check-customer-apk start ..."
			#delete amlogic dvb package     
			#echo "delete amlogic dvb packages..."
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/DVBService*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/DVBPlayer*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/bookplay_package*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/progmanager*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/dvbsearch*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/dvbepg*
			#rm ${DIR_PRODUCT_OUTPUT}/system/app/dvbdemotest*
		
			if [ "${SOWELL_CUSTOMER_NAME}" == "ott-sample" ] || [ "${SOWELL_CUSTOMER_NAME}" == "htv-zh" ] ; then
				echo -e "\033[0;35m Copy Launcher For HTV\033[0m"
				cp ${CUR_DIR}/vendor/sowell/prebuilt/HtvLauncher.apk ${DIR_PRODUCT_OUTPUT}/system/app/
			else
				echo -e "\033[0;35m Copy Launcher For !HTV\033[0m"
				cp ${CUR_DIR}/vendor/sowell/prebuilt/SwlLauncher2.apk ${DIR_PRODUCT_OUTPUT}/system/app/
			fi


#			if [ "${SOWELL_FACTORY_MODE}" = "true" ]; then
#				echo -e "\033[0;35m For factory \033[0m"
#				mv ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2.apk ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2apk
#				mv ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2.odex ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2odex
			#	mv ${DIR_PRODUCT_OUTPUT}/system/app/HtvLauncher.apk ${DIR_PRODUCT_OUTPUT}/system/app/HtvLauncherapk
#			else 
#				echo -e "\033[0;35m For Normal mode \033[0m"
#				echo "sign apk for Test "
				#if [  -f ${DIR_PRODUCT_OUTPUT}/system/app/Test.apk ]; then
					#java -jar $ANDROID_BUILD_TOP/out/host/linux-x86/framework/signapk.jar -w $ANDROID_BUILD_TOP/device/amlogic/$TARGET_PRODUCT/keystore/platform.x509.pem $ANDROID_BUILD_TOP/device/amlogic/$TARGET_PRODUCT/keystore/platform.pk8 ${DIR_PRODUCT_OUTPUT}/system/app/Test.apk ${DIR_PRODUCT_OUTPUT}/system/app/Test.apk 
				#fi
#				mv ${DIR_PRODUCT_OUTPUT}/system/app/Test.apk ${DIR_PRODUCT_OUTPUT}/system/app/Testapk
#				mv ${DIR_PRODUCT_OUTPUT}/system/app/Test.odex ${DIR_PRODUCT_OUTPUT}/system/app/Testodex
#				if [ -f ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2apk ] || [ -f ${DIR_PRODUCT_OUTPUT}/system/system/app/HtvLauncherapk ];then
#					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2apk
#					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2odex
#					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/HtvLauncherapk
#				fi
#			fi

			if [ "${NO_DVB}" == "true" ]; then
				echo "no dvb"
				rm ${DIR_PRODUCT_OUTPUT}/system/app/SwlDvb*
			fi
			
			if [ "${NO_FTV}" == "true" ]; then
					echo "no ftv"
					rm ${DIR_PRODUCT_OUTPUT}/system/app/SwlFtv*
			fi				

			if [ "${NO_OSCAM}" == "true"  ]; then
					echo "no oscam" 
					if [  -f ${DIR_PRODUCT_OUTPUT}/system/app/Share.apk ]; then
						rm -rf  ${DIR_PRODUCT_OUTPUT}/system/app/Share.apk 
					fi
					if [  -f ${DIR_PRODUCT_OUTPUT}/system/bin/oscam-static ]; then
						rm -rf  ${DIR_PRODUCT_OUTPUT}/system/bin/oscam-static
					fi
			else 
					echo "built-in oscam into system"
					mk-oscam
			fi
		
			#delete HTV apps from system apps start
			if [ "${NO_HTV}" == "true" ]; then
					echo "That's mean use old code, Not htv apps in system"
					for i in $HTV_PREBUILT_APPS; do
						rm ${DIR_PRODUCT_OUTPUT}/system/app/$i.apk
						rm ${DIR_PRODUCT_OUTPUT}/system/app/$i.odex
					done
			fi
			#delete HTV apps from system apps end


			if [ "${SOWELL_CUSTOMER_NAME}" == "ott-sample" ] || [ "${SOWELL_CUSTOMER_NAME}" == "htv-zh" ] ; then
				echo "Delete OOBE.apk , Swl APPS(that's not in HTV system)" 
				TMPAPPS="OOBE SwlDvb SwlFtv SwlLauncher2 SwlMyAPP Launcher2 CxTvSettings HtvWelcome"
				for i in $TMPAPPS; do
					rm -rf ${DIR_PRODUCT_OUTPUT}/system/app/$i.apk
					rm -rf ${DIR_PRODUCT_OUTPUT}/system/app/$i.odex 
				done
			fi

			extractJniLib


			#copy dvblib for HelloWorld
			echo "Copy file libzvb.so to system/lib"
	 		cp	${CUR_DIR}/packages/sowell/code/swlpackage/dvblib/libzvbi.so ${DIR_PRODUCT_OUTPUT}/system/lib/

        	echo -e "\033[0;35m Build Sowell app or bin\033[0m"
			touch ${CUR_DIR}/packages/sowell/code/swlpackage/Helloworld/Common/sw_config.cpp
			touch ${CUR_DIR}/packages/sowell/code/swlpackage/Helloworld/HelloWorld.cpp
        	cd ${CUR_DIR}/packages/sowell/code/swlpackage/SwlJavalibs/
			mm
        	cd ${CUR_DIR}/packages/sowell/prebuilt/
        	mm
			cd ${CUR_DIR}/vendor/sowell/prebuilt/
        	mm

			if [ "${SOWELL_FACTORY_MODE}" = "true" ]; then
				echo -e "\033[0;35m For factory \033[0m"
				mv ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2.apk ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2apk
				mv ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2.odex ${DIR_PRODUCT_OUTPUT}/system/app/SwlLauncher2odex
				mv ${DIR_PRODUCT_OUTPUT}/system/app/HtvLauncher.apk ${DIR_PRODUCT_OUTPUT}/system/app/HtvLauncherapk
			else 
				echo -e "\033[0;35m For Normal mode \033[0m"
				mv ${DIR_PRODUCT_OUTPUT}/system/app/Test.apk ${DIR_PRODUCT_OUTPUT}/system/app/Testapk
				mv ${DIR_PRODUCT_OUTPUT}/system/app/Test.odex ${DIR_PRODUCT_OUTPUT}/system/app/Testodex
				if [ -f ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2apk ] || [ -f ${DIR_PRODUCT_OUTPUT}/system/system/app/HtvLauncherapk ];then
					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2apk
					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/SwlLauncher2odex
					rm ${DIR_PRODUCT_OUTPUT}/system/system/app/HtvLauncherapk
				fi

			fi

	croot	
	echo "check-customer-apk end ..."
}



mk-otapackage()
{	
	echo "make otapackage start ..."
	if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then
		make otapackage -j12
	else
		echo -e "\033[1;40;31m"make otapackage  fail"\033[0m\n"
	fi
	echo "make otapackage end ..."
}

sign-recovery()
{
	if [ ! -d $DIR_PRODUCT_OUTPUT/recovery/root ]; then
		echo "No $DIR_PRODUCT_OUTPUT/recovery/root found! You need build it first"
		echo "make recoveryimage at android top dir"
	else
		echo "Sign customer key for recovery start" $SOWELL_ANDROID_CONFIG_NAME
		java -jar ${CUR_DIR}/out/host/linux-x86/framework/dumpkey.jar ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/keystore/customerkey.x509.pem > ${ANDROID_PRODUCT_OUT}/recovery/root/res/keys
		echo "Sign customer key for recovery stop"
	fi
	mk-recovery
}

sign-apk()
{			
	#sign apk use our key.
	echo "resign target apk..."
	${CUR_DIR}/build/tools/releasetools/sign_target_files_apks -d ${DIR_KEY} -e GooglePlayStore.apk= -e GoogleLoginService.apk= -e GoogleServicesFramework.apk=  \
	-e oem_install_flash_player_jb_mr1.apk= -e MboxSettings.apk=  -e MediaBoxLauncher.apk=  -e Miracast.apk= -e OpenWnn.apk=  -e DLNA.apk=  -e OneClickCleaner.apk= \
	-e DoonungonBox.apk= -e LeoTechStore.apk= -e 3BBCloudIPTV.apk= \
	-e xiamimusic.apk= -e MoreTV_0.3.1_1128.apk= -e XCgamecenter.apk= \
	-e AuthService.apk= -e CxTvLive.apk= -e CxTvMarket.apk=  -e CxTvSettings.apk=${DIR_KEY}/platform \
	-e HtvLauncher.apk= \
	-e HtvWelcome.apk= \
	-e RemoteServer.apk=${DIR_KEY}/platform \
	-e Share.apk= \
	-e SwlDvb.apk=${DIR_KEY}/platform \
	-e OOBE.apk=${DIR_KEY}/platform \
	-e Test.apk=${DIR_KEY}/platform \
	-e SwlFtv.apk= -e SwlMyAPP.apk=   -e SwlNetNavigation.apk= -e SwlMarket2.apk= -e SwlUserManual.apk= -e SwlLauncher2.apk= -e SwlTvOnline.apk=  -e SwlNetVideos.apk=  -e SwlUpgrade.apk= \
	-o ${CUR_DIR}/out/target/product/${SOWELL_ANDROID_CONFIG_NAME}/obj/PACKAGING/target_files_intermediates/${SOWELL_ANDROID_CONFIG_NAME}-target_files-${TMPDATE}.zip 	target_files_resigned.zip

}

sign-otapackage()
{
	echo "sign-otapackage..."
	cd ${CUR_DIR}
	tmp_zip=$DIR_PRODUCT_OUTPUT/obj/PACKAGING/target_files_intermediates/$TARGET_PRODUCT-target_files-`date +%Y%m%d`.zip
	echo "ota target file:mx-ota-full-update-${SOWELL_CUSTOMER_NAME}-$USER-$DATE.zip ..........."
#echo ${CUR_DIR}/build/tools/releasetools/ota_from_target_files -v --amlogic -p ${CUR_DIR}/out/host/linux-x86 -k ${DIR_KEY}/customerkey target_files_resigned.zip mx-ota-full-update-${SOWELL_CUSTOMER_NAME}-$USER-$DATE.zip	
	${CUR_DIR}/build/tools/releasetools/ota_from_target_files -v -p ${CUR_DIR}/out/host/linux-x86 -k ${DIR_KEY}/customerkey $tmp_zip mx-ota-full-update-${SOWELL_CUSTOMER_NAME}-$USER-$DATE.zip	
		
	echo "sign-otapackage end..."

}

mk-customer-package()
{
	echo "make customer otapackage start..."
        if [ "${SOWELL_CONFIG_FLAG}" = "true" ]; then
			DATE=`date +%Y.%m.%d-%k.%M|sed s/\ //`;
			USER=`whoami`;
			TMPDATE=`date +%Y%m%d`
			echo ${TMPDATE}
					
			#copy dvblib for HelloWorld
			echo "Copy file libzvb.so to system/lib"
	 		cp	${CUR_DIR}/packages/sowell/code/swlpackage/dvblib/libzvbi.so ${DIR_PRODUCT_OUTPUT}/system/lib/
			check-customer-apk
			#sign-apk
			mk-otapackage
        else
            echo "not setup config..."
        fi

        echo "make customer otapackage end..."
}

mk-sign-otapackage()
{
	sign-recovery
	sign-apk
	sign-otapackage
}


if [ $# -gt 0 ]; then
	#cd packages/sowell/code/swlpackage/Helloworld
	#./Runfirst.sh
	cd ${CUR_DIR}
	unset SOWELL_CUSTOMER_NAME

	# remove old customer data
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/bootanimation.zip
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/remote.conf
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/BoardConfig.mk
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/system.prop
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/CustomerConfig.mk
	rm ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/keystore/customerkey.*
	
	if [ $1 == "ott-sample" ] || [ $1 == "dvb-sample" ] || [ $1 == "htv-zh" ] ; then
		export SOWELL_CUSTOMER_NAME=$1
		echo ${SOWELL_CUSTOMER_NAME}
		cp  ${CUR_DIR}/customer-config/$1/* ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}
#		cp  ${CUR_DIR}/customer-config/$1/keystore/* ${CUR_DIR}/device/amlogic/${SOWELL_ANDROID_CONFIG_NAME}/keystore/
	else
		echo "unknow customer name..........."
		return
	fi
	echo -e "\033[1;40;32m========================================================="
	echo -e "\033[1;40;32mSOWELL_CUSTOMER_NAME: ${SOWELL_CUSTOMER_NAME}"
	
	#config for factory.
	if [ $# -gt 1 ]; then
		if [ $2 == "factory" ]; then
			SOWELL_FACTORY_MODE=true;
			echo "SOWELL_FACTORY_MODE ${SOWELL_FACTORY_MODE}"
		else
			echo -e "\033[1;40;31mThat's mean : Normal mode , not Factory...\033[0m\n"
		fi
	fi
	
	export SOWELL_FACTORY_MODE=${SOWELL_FACTORY_MODE}	

	# config app by customer.
	if [ "${SOWELL_CUSTOMER_NAME}" == "ott-sample" ]; then
			NO_DVB=true;
			NO_FTV=true;
			NO_OSCAM=true;
			NO_HTV=false;
	fi
	
	if [ "${SOWELL_CUSTOMER_NAME}" == "htv-zh" ]; then
			NO_DVB=true;
			NO_FTV=true;
			NO_OSCAM=true;
			NO_HTV=false;
	fi
	
	if [ "${SOWELL_CUSTOMER_NAME}" == "dvb-sample" ]; then
			NO_DVB=false;
			NO_FTV=false;
			NO_OSCAM=false;
			NO_HTV=true;
	fi
	
	echo "SOWELL_FACTORY_MODE      = ${SOWELL_FACTORY_MODE}"
	echo "NO_DVB       		= ${NO_DVB}"
	echo "NO_FTV       		= ${NO_FTV}"
	echo "NO_OSCAM     		= ${NO_OSCAM}"
	echo "NO_HTV			= ${NO_HTV}"
	DATE=`date +%Y.%m.%d-%k.%M|sed s/\ //`;
	echo "package name:ota-full-update-${SOWELL_CUSTOMER_NAME}-$USER-$DATE.zip"	
	echo -e "==========================================================\033[0m"


	touch packages/sowell/code/swlpackage/Helloworld/Common/sw_config.cpp
	touch packages/sowell/code/swlpackage/Helloworld/HelloWorld.cpp
    setup-config
else
	echo -e "\033[1;40;35mparam error...\033[0m\n"
	show-usage	
fi

