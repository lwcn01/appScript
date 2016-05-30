package com.sugar.builder;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;


public class DevicesHelper {
	
	//设备状态
	public static enum DevicesStatus {
		device,							//正常情况
		host,							//有些时候模拟器会是这种状态
		offline,						//设备离线,一般是线没有插好
		unauthorized,					//未认证，手机端未勾选use调试
		unknown							//未知
	}
	
	/**
	 * 把从输出流解析出的设备状态格式化成DevicesStatus
	 * @param status
	 * @return
	 */
	public static DevicesStatus formatDeviceStatus(String status) {
		if(status == null || status.isEmpty()) {
			return DevicesStatus.unknown;
		} else if ("device".equalsIgnoreCase(status)) {
			return DevicesStatus.device;
		} else if ("unauthorized".equalsIgnoreCase(status)) {
			return DevicesStatus.unauthorized;
		} else if ("offline".equalsIgnoreCase(status)) {
			return DevicesStatus.offline;
		} else if ("host".equalsIgnoreCase(status)) {
			return DevicesStatus.host;
		} else {
			return DevicesStatus.unknown;
		}
	}
	
	/***
	 * 把设备状态转换成可读的字符串形式，一般用于debug
	 * @param devicesStatus
	 * @return
	 */
	public static String formatDeviceStatus(DevicesStatus devicesStatus) {
		String status = "";
		
		switch (devicesStatus) {
		case device:
			status = "device";
			break;
		case unauthorized:
			status = "unauthorized";
			break;
		case offline:
			status = "offline";
			break;	
		case host:
			status = "host";
			break;	
		default:
			status = "unknown";
			break;
		}
		
		return status;
	}
	
	/***
	 * 设备信息
	 * @author johnny
	 *
	 */
	public static class DevicesInfo implements Serializable {

		/**
		 * 
		 */
		private static final long serialVersionUID = -101058288969022611L;
	
		private String mDevicesName;						//设备名
		private DevicesStatus mDevicesStatus;				//设备状态
		
		public DevicesInfo(String devicesName, DevicesStatus status) {
			mDevicesName = devicesName;
			mDevicesStatus = status;
		}
		
		public DevicesInfo(String devicesId){
			this(devicesId, DevicesStatus.unknown);
		}
		
		public String getDevicesName() {
			return mDevicesName;
		}

		public DevicesInfo setDevicesName(String name) {
			this.mDevicesName = name;
			return this;
		}

		public DevicesStatus getDevicesStatus() {
			return mDevicesStatus;
		}

		public DevicesInfo setDevicesStatus(DevicesStatus status) {
			this.mDevicesStatus = status;
			return this;
		}
		
		@Override
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append("{").append("device name[").append((mDevicesName == null? "null":mDevicesName))
			.append("]");
			sb.append(", devices status[").append(formatDeviceStatus(mDevicesStatus)).append("]}");
			return sb.toString();
		}	
	}
	
	public static class DeviceNotFoundException extends Exception{

		/**
		 * 
		 */
		private static final long serialVersionUID = 6175630687026321840L;
		
		public DeviceNotFoundException(String msg) {
			super(msg);
		}
		
	}
	
	/***
	 * 执行adb命令后,返回的结果解析接口
	 * @author johnny
	 * @param <T>
	 */
	public interface CmdResultHandler<T> {
		/***
		 * 
		 * @param resultStream		执行adb命令后返回的结果流
		 * @return
		 */
		public T handleCmdResult(InputStream resultStream);
	}
	
	//默认的结果解析接口实现,仅仅是向控制台输出adb返回的内容
	private static final CmdResultHandler<Void> DEFAULT_CMD_RESULT_HANDLER = new CmdResultHandler<Void>() {

		@Override
		public Void handleCmdResult(InputStream resultStream) {
			String line = null;
			BufferedReader br = null;
			StringBuilder sb = new StringBuilder();
			try {
				br = new BufferedReader(new InputStreamReader(resultStream));
				while((line = br.readLine()) != null) {
					sb.append(line);
				}
				System.out.println(sb.toString());
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				Util.safeClose(br);
			}
			return null;
		}
	};
	
	/***
	 * 执行命令, 该函数为同步函数
	 * @param cmd	需要执行的命令
	 */
	public static void executeCmd(String[] cmd){
		executeCmd(cmd, DEFAULT_CMD_RESULT_HANDLER);
	}
	
	/***
	 * 执行命令, 该函数为同步函数
	 * @param cmd					需要执行的命令
	 * @param resultHandler			命令返回结果解析handler
	 * @return
	 */
	public static <T> T executeCmd(String[] cmd, CmdResultHandler<T> resultHandler) {
		Process p = null;
		try {
			p = Runtime.getRuntime().exec(cmd);
			return resultHandler.handleCmdResult(p.getInputStream());
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			safeDestroyProcess(p);
		}
		
		return null;
	}
	
	/***
	 * 异步执行命令
	 * @param cmd
	 */
	public static <T> void asyncExecuteCmd(final String[] cmd){
		asyncExecuteCmd(cmd, DEFAULT_CMD_RESULT_HANDLER);
	}
	
	/***
	 * 异步执行命令
	 * @param cmd
	 */
	public static <T> void asyncExecuteCmd(final String[] cmd, final CmdResultHandler<T> resultHandler) {
		ExecutorService executor = Executors.newSingleThreadExecutor();
		Runnable r = new Runnable() {
			
			@Override
			public void run() {
				executeCmd(cmd, resultHandler);
			}
		};
		executor.execute(r);
		executor.shutdown();
	}
	
	/***
	 * 设备过滤器
	 * @author johnny
	 *
	 */
	public static interface DevicesFilter {
		/***
		 * 如果需要包含这个设备则返回true,如果要过滤返回false
		 * @param devicesName			设备名
		 * @param devicesStatus			设备状态
		 * @return
		 */
		boolean accept(String devicesName, DevicesStatus devicesStatus);
	}
	
	/**
	 * 通过adb命令查找设备(包含所有状态的设备)
	 * @return
	 */
	public static List<DevicesInfo> findDevices() {
		return findDevices(null);
	}
	
	/**
	 * 通过adb命令查找设备
	 * @return
	 */
	public static List<DevicesInfo> findDevices(final DevicesFilter filter) {
		CmdResultHandler<List<DevicesInfo>>  devicesHandler = new CmdResultHandler<List<DevicesInfo>>() {

			@Override
			public List<DevicesInfo> handleCmdResult(InputStream resultStream) {
				List<DevicesInfo> devicesInfos = new ArrayList<DevicesHelper.DevicesInfo>(4);
				if(resultStream == null) {
					return devicesInfos;
				}
				
				String line = "";
				BufferedReader br = null;
				try {
					br = new BufferedReader(new InputStreamReader(resultStream));
					//一直读到"List of devices attached"出现后, 后面的行才是设备信息
					for (;!line.trim().equalsIgnoreCase("List of devices attached"); line = br.readLine());
					if(line.trim().equalsIgnoreCase("List of devices attached")) {
						while((line = br.readLine()) != null) {
							String[] devicesInfo = line.split("\\s+");
							if(devicesInfo != null && devicesInfo.length == 2) {
								String devicesName = devicesInfo[0].trim();
								DevicesStatus devicesStatus = formatDeviceStatus(devicesInfo[1].trim());
								if(filter != null) {
									if(filter.accept(devicesName, devicesStatus)){
										devicesInfos.add(new DevicesInfo(devicesName, devicesStatus));
									}
								} else {
									devicesInfos.add(new DevicesInfo(devicesName, devicesStatus));
								}
							}
						}
					}
				} catch (IOException e) {
					e.printStackTrace();
				} finally {
					Util.safeClose(br);
				}
				return devicesInfos;
			}
		};
		
		Process p = null;
		List<DevicesInfo> devicesInfos = Collections.emptyList();
		try {
			p = Runtime.getRuntime().exec(new String[]{"adb", "devices"});
			devicesInfos = devicesHandler.handleCmdResult(p.getInputStream());
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			safeDestroyProcess(p);
		}
		
		return devicesInfos;
	}
	
	private static final DevicesFilter CONNECTED_DEVICES_FILTER = new DevicesFilter() {
		
		@Override
		public boolean accept(String devicesName, DevicesStatus devicesStatus) {
			return DevicesStatus.device == devicesStatus;
		}
	};
	
	/**
	 * 查找所有已连接上的设备
	 * @return
	 */
	public static List<DevicesInfo> findConnectedDevices() {
		return findDevices(CONNECTED_DEVICES_FILTER);
	}
	
	/***
	 * 是否有设备连接成功
	 * @return
	 */
	public static boolean isDeviceConnected() {
		return findConnectedDevices().size() > 0;
	}
	
	private static Set<String> sPushFailedDevices= null;			//push失败的设备列表
	private static final class PushFileRunnable implements Runnable,CmdResultHandler<Boolean> {
		
		private final CountDownLatch countDownLatch;
		private DevicesInfo devices;
		private String localFile;
		private String sdcardFile;
		
		PushFileRunnable(CountDownLatch countDownLatch, DevicesInfo devices, 
				String localFile, String sdcardFile) {
			this.countDownLatch = countDownLatch;
			this.devices = devices;
			this.localFile = localFile;
			this.sdcardFile = sdcardFile;
		}
		
		@Override
		public void run() {
			Process p = null;
			try {
				p = Runtime.getRuntime().exec(new String[] {"adb", "-s", devices.getDevicesName(),
						"push", localFile, sdcardFile});
				if(handleCmdResult(p.getInputStream())) {
					synchronized (sPushFailedDevices) {
						sPushFailedDevices.add(devices.getDevicesName());
					}
					System.out.println(String.format("push file [from %s to device: %s, device path: %s failed", 
							localFile, devices.getDevicesName(), sdcardFile));
				} else {
					System.out.println(String.format("push file [from %s to device: %s, device path: %s success", 
							localFile, devices.getDevicesName(), sdcardFile));
				}
				p.waitFor();
			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			} finally {
				countDownLatch.countDown();
				safeDestroyProcess(p);
			}
		}

		@Override
		public Boolean handleCmdResult(InputStream resultStream) {
			String line = null;
			BufferedReader br = null;
			boolean errorAppeared = false;
			try {
				br = new BufferedReader(new InputStreamReader(resultStream));
				while((line = br.readLine()) != null) {
					if(line.contains("error") || line.contains("failed") || line.contains("cannot")) {
						errorAppeared = true;
						break;
					}
				}
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				Util.safeClose(br);
			}
			return errorAppeared;
		}
		
	}
	
	public static boolean pushFileToSdcard(String localFile, String sdcardPath) 
			throws DeviceNotFoundException{
		return pushFileToSdcard(findConnectedDevices(), localFile, sdcardPath, 60 * 1000);
	}
	
	public static boolean pushFileToSdcard(List<DevicesInfo> devicesList, 
			String localFile, String sdcardPath) 
			throws DeviceNotFoundException{
		return pushFileToSdcard(devicesList, localFile, sdcardPath, 60 * 1000);
	}
	
	/***
	 * 把文件push到sd卡
	 * @param devicesList			需要push的设备列表，可以通过findConnectedDevices获取所有已连接的设备
	 * @param localFile				需要push到sd卡的本地文件全路径
	 * @param sdcardPath			需要push文件到sd的路径
	 * @param timeout				push超时时间
	 * @return						全部成功返回true, 否则返回false,可以通过getPushFailedDevices查看push失败的设备
	 * @throws DeviceNotFoundException
	 */
	public static boolean pushFileToSdcard(List<DevicesInfo> devicesList, 
			String localFile, String sdcardPath, long timeout) 
			throws DeviceNotFoundException{
		
		if(devicesList.isEmpty()) {
			throw new DeviceNotFoundException("not found connected devices");
		}
		
		if(sPushFailedDevices == null) {
			sPushFailedDevices = new HashSet<String>();
		}
		
		if(!sPushFailedDevices.isEmpty()){
			sPushFailedDevices.clear();
		}
		
		Thread[] threads = new Thread[devicesList.size()];
		CountDownLatch countDownLatch = new CountDownLatch(devicesList.size());
		System.out.println(String.format("开启%s个线程执行命令", threads.length));
		for (int i = 0; i < threads.length; i++) {
			threads[i] = new Thread(
					new PushFileRunnable(countDownLatch, devicesList.get(i), localFile, sdcardPath), 
										"Push--Thread--" + i);
			threads[i].start();
		}
		
		try {
			countDownLatch.await(timeout, TimeUnit.MILLISECONDS);
		} catch (InterruptedException e) {
			e.printStackTrace();
			return false;
		}
		
		synchronized (sPushFailedDevices) {
			return sPushFailedDevices.isEmpty();
		}
	}
	
	public static Set<String> getPushFailedDevices() {
		synchronized (sPushFailedDevices) {
			if(sPushFailedDevices == null) {
				sPushFailedDevices = new HashSet<String>(0);
			}
			return sPushFailedDevices;
		}
	}
	
	private static final void safeDestroyProcess(Process p) {
		if(p != null) {
			p.destroy();
		}
	}
}
