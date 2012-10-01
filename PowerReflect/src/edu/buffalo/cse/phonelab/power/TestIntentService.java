package edu.buffalo.cse.phonelab.power;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;

import edu.buffalo.cse.phonelab.lib.BatteryStatsImpl;
import edu.buffalo.cse.phonelab.lib.PowerProfile;
import edu.buffalo.cse.phonelab.lib.ReflectionUtils;
import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.hardware.SensorManager;
import android.os.SystemClock;
import android.util.Log;
import android.util.SparseArray;

public class TestIntentService extends IntentService {

		
		public TestIntentService() {
			super("TestIntentService");
		}
	
	String TAG = "TestIntent";
	

	@Override
	protected void onHandleIntent(Intent intent) {
		// TODO Auto-generated method stub
		
		Log.v(TAG,"Service Started");
		//Class<?> Timer = Class.forName("android.os.BatteryStats$Timer");
		BatteryStatsImpl mStats = new BatteryStatsImpl();
		PowerProfile mPowerProfile = new PowerProfile(getApplicationContext());
		int mStatsType = 0;
		try{
			mStatsType = (Integer) ReflectionUtils.getStaticValue("android.os.BatteryStats", "STATS_SINCE_UNPLUGGED");
		}catch(Exception e)
		{
			mStatsType = 3;
			Log.e(TAG,"When it all started: "+e);
		}
     
        try{
		//variables according to powerAppUsage
		SensorManager sensorManager = (SensorManager)getApplicationContext().getSystemService(
                Context.SENSOR_SERVICE);
        final int which = mStatsType;
        final int speedSteps = (Integer)mPowerProfile.invoke("getNumSpeedSteps",(Object[]) null);
        final double[] powerCpuNormal = new double[speedSteps];
        final long[] cpuSpeedStepTimes = new long[speedSteps];
        for (int p = 0; p < speedSteps; p++) {
            powerCpuNormal[p] = (Double) mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_CPU_ACTIVE"), p);
        }
        double appWakelockTime = 0;
        long uSecTime = (Long) mStats.invoke("computeBatteryRealtime",SystemClock.elapsedRealtime() * 1000, which);
		Log.i(TAG, "uSecTime = "+uSecTime);
		
		final long uSecNow = (Long)mStats.invoke("computeBatteryRealtime",uSecTime, which);
        final long timeSinceUnplugged = uSecNow;
        Log.i(TAG, "Uptime since last unplugged = " + (timeSinceUnplugged / 1000));
        		
       	double averageCostPerByte = 0.0;
    	double mAppWifiRunning = (double) 0.0;

		//Average cost per byte Calculation
		try{
		
			long WIFI_BPS = 1000000; // TODO: Extract average bit rates from system 
			long MOBILE_BPS = 200000; // TODO: Extract average bit rates from system
        
			double WIFI_POWER = (Double) mPowerProfile.invoke("getAveragePower", mPowerProfile.getValue("POWER_WIFI_ACTIVE"))/3600; 
			double MOBILE_POWER = (Double) mPowerProfile.invoke("getAveragePower", mPowerProfile.getValue("POWER_RADIO_ACTIVE")) ;
			long mobileData = (Long) mStats.invoke("getMobileTcpBytesReceived",mStatsType) + (Long) mStats.invoke("getMobileTcpBytesSent",mStatsType);
			long wifiData = (Long) mStats.invoke("getTotalTcpBytesReceived",mStatsType) + (Long)mStats.invoke("getTotalTcpBytesSent",mStatsType) - mobileData;
			long radioDataUptimeMs = (Long)mStats.invoke("getRadioDataUptime", (Object [])null) / 1000;
			long mobileBps = radioDataUptimeMs != 0 ? mobileData * 8 * 1000 / radioDataUptimeMs : MOBILE_BPS;

			double mobileCostPerByte = MOBILE_POWER / (mobileBps / 8);
			double wifiCostPerByte = WIFI_POWER / (WIFI_BPS / 8);
			if (wifiData + mobileData != 0) {
				averageCostPerByte = (mobileCostPerByte * mobileData + wifiCostPerByte * wifiData) / (mobileData + wifiData);
				} else {
					averageCostPerByte = 0.0;
				}
			Log.i(TAG, WIFI_POWER+" , "+MOBILE_POWER+"  ,  "+mobileData+"  ,  "+wifiData);
			Log.i(TAG, "The average Data cost is "+averageCostPerByte);
		}catch(Exception e)
		{
			Log.e(TAG, "Error yet again "+e);
		}
		
		//Getting all Uids and the mapping
		
		Object uidStats = mStats.invoke("getUidStats", (Object[]) null);
		/**
         * Calling SparseArray.size() within the instance uidStats. 
         */
		try {
			int NU = (Integer) ReflectionUtils.invoke(uidStats, "size", (Object[]) null);
			Log.v(TAG, "uidStats.size(): " + NU);
        /**
         * Getting all process names using Uid.
         */
			for (int iu = 0; iu < NU; iu++) 
			{
				 Object u;
				 double power = 0;
		         double highestDrain = 0;
		         String packageWithHighestDrain = null;
		         
				 u = ReflectionUtils.invoke(uidStats, "valueAt", iu);
				 Object uid = ReflectionUtils.invoke(u, "getUid", (Object []) null);
				 Log.i(TAG,"Current Uid: "+uid);
					Map<String, ?> processStats = (Map<String, ?>) ReflectionUtils.invoke(u, "getProcessStats", (Object[]) null);
					long cpuTime = 0;
		            long cpuFgTime = 0;
		            long wakelockTime = 0;
		            long gpsTime = 0;

					if (processStats.size() > 0) {
						for (Map.Entry<String, ?> ent: processStats.entrySet()) 
						{
							//Log.v(TAG, "Process name = " + ent.getKey());
							Object ps  = ent.getValue();
							long userTime = (Long)ReflectionUtils.invoke(ps,"getUserTime",which);
							long systemTime = (Long)ReflectionUtils.invoke(ps,"getSystemTime",which);
							long foregroundTime = (Long)ReflectionUtils.invoke(ps,"getForegroundTime",which);
							cpuFgTime += foregroundTime * 10; // convert to millis
							long tmpCpuTime = (userTime + systemTime) * 10; // convert to millis
							
							int totalTimeAtSpeeds = 0;
		                    // Get the total first
		                    for (int step = 0; step < speedSteps; step++) {
		                        cpuSpeedStepTimes[step] = (Long) ReflectionUtils.invoke(ps,"getTimeAtCpuSpeedStep",step, which);
		                        totalTimeAtSpeeds += cpuSpeedStepTimes[step];
		                    }
		                    
		                    if (totalTimeAtSpeeds == 0) totalTimeAtSpeeds = 1;
		                    // Then compute the ratio of time spent at each speed
		                    double processPower = 0;
		                    for (int step = 0; step < speedSteps; step++) {
		                        double ratio = (double) cpuSpeedStepTimes[step] / totalTimeAtSpeeds;
		                        processPower += ratio * tmpCpuTime * powerCpuNormal[step];
		                    }
		                    cpuTime += tmpCpuTime;
		                    power += processPower;

		                    if (packageWithHighestDrain == null
		                            || packageWithHighestDrain.startsWith("*")) {
		                        highestDrain = processPower;
		                        packageWithHighestDrain = ent.getKey();
		                    } else if (highestDrain < processPower
		                            && !ent.getKey().startsWith("*")) {
		                        highestDrain = processPower;
		                        packageWithHighestDrain = ent.getKey();
		                        Log.v(TAG, "Max drain of " + highestDrain + " by " + packageWithHighestDrain);
		                    }
		                   
				          
		                    Log.i(TAG, "Process name = " + ent.getKey()+ "cputime -->"+ cpuTime);
		                }
		                 
		            }
		            if (cpuFgTime > cpuTime) {
		                if (cpuFgTime > cpuTime + 10000) {
		                    Log.i(TAG, "WARNING! Cputime is more than 10 seconds behind Foreground time");
		                }
		                cpuTime = cpuFgTime; // Statistics may not have been gathered yet.
		            }
		            power /= 1000;


		            // Process wake lock usage
		            Map<String, ? > wakelockStats = (Map<String, ?>) ReflectionUtils.invoke(u,"getWakelockStats",(Object []) null);
		            for (Map.Entry<String, ? > wakelockEntry : wakelockStats.entrySet()) {
		                Object wakelock = wakelockEntry.getValue();
		                // Only care about partial wake locks since full wake locks
		                // are canceled when the user turns the screen off.
		                Object timer = ReflectionUtils.invoke(wakelock,"getWakeTime",ReflectionUtils.getStaticValue("android.os.BatteryStats","WAKE_TYPE_PARTIAL"));
		                
		                if (timer != null) {
		                    wakelockTime += (Long)ReflectionUtils.invoke(timer,"getTotalTimeLocked", uSecTime, which);
		                }
		            }
		            wakelockTime /= 1000; // convert to millis
		            appWakelockTime += wakelockTime;

		            // Add cost of holding a wake lock
		                    power += (wakelockTime
		                    * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_CPU_AWAKE"))) / 1000;

		            // Add cost of data traffic
		            long tcpBytesReceived = (Long) ReflectionUtils.invoke(u,"getTcpBytesReceived",mStatsType);
		            long tcpBytesSent = (Long) ReflectionUtils.invoke(u,"getTcpBytesSent",mStatsType);
		            power += (tcpBytesReceived+tcpBytesSent) * averageCostPerByte;

		            // Add cost of keeping WIFI running.
		            long wifiRunningTimeMs = (Long)ReflectionUtils.invoke(u,"getWifiRunningTime",uSecTime, which) / 1000;
		            mAppWifiRunning += wifiRunningTimeMs;
		            power += (wifiRunningTimeMs
		                    * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_WIFI_ON"))) / 1000;

					
		            // Process Sensor usage
		            Map<Integer, ? > sensorStats = (Map<Integer, ?>) ReflectionUtils.invoke(u,"getSensorStats",(Object []) null);
		            for (Map.Entry<Integer, ? > sensorEntry : sensorStats.entrySet()) {
		                Object sensor = sensorEntry.getValue();
		                int sensorType = (Integer)ReflectionUtils.invoke(sensor, "getHandle", (Object []) null);
		                Object timer = ReflectionUtils.invoke(sensor,"getSensorTime",(Object []) null);
		                long sensorTime = (Long)ReflectionUtils.invoke(timer,"getTotalTimeLocked",uSecTime, which) / 1000;
		                double multiplier = 0;
		                switch (sensorType) {
	//	                    case (Integer) ReflectionUtils.getStaticValue("android.os.BatterStats$Sensor", "GPS"):
		                	case -10000:
		                        multiplier = (Double) mPowerProfile.invoke("getAveragePower", mPowerProfile.getValue("POWER_GPS_ON"));
		                        gpsTime += sensorTime;
		                        break;
		                    default:
		                        android.hardware.Sensor sensorData =
		                                sensorManager.getDefaultSensor(sensorType);
		                        if (sensorData != null) {
		                            multiplier = sensorData.getPower();
		                            Log.i(TAG, "Got sensor " + sensorData.getName() + " with power = "+ multiplier);
		                            
		                        }
		                }
		                power += (multiplier * sensorTime) / 1000;
		            }
            
		            Log.i(TAG, "All details " + power+ " --- Wifi Running = "+mAppWifiRunning+"----Wakelock Time = "+appWakelockTime+"----GPS Time = "+gpsTime);
		            
			}
			

		} catch (NoSuchMethodException e) {
			// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (InvocationTargetException e) {
			// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
            
			//Add Phone Usage
			long phoneOnTimeMs = (Long)mStats.invoke("getPhoneOnTime",uSecNow, mStatsType) / 1000;
	        double phoneOnPower = (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_RADIO_ACTIVE")) * phoneOnTimeMs / 1000;
	        Log.i(TAG,"Power due to Phone Usage: "+phoneOnPower);
        	
	        //Add Screen Usage
	        double power = 0;
	        long screenOnTimeMs = (Long)mStats.invoke("getScreenOnTime",uSecNow, mStatsType) / 1000;
	        power += screenOnTimeMs * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_SCREEN_ON"));
	        final double screenFullPower =
	                (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_SCREEN_FULL"));
	        for (int i = 0; i < (Integer)ReflectionUtils.getStaticValue("android.os.BatteryStats","NUM_SCREEN_BRIGHTNESS_BINS"); i++) {
	            double screenBinPower = screenFullPower * (i + 0.5f)
	                    / (Integer)ReflectionUtils.getStaticValue("android.os.BatteryStats","NUM_SCREEN_BRIGHTNESS_BINS");
	            long brightnessTime = (Long)mStats.invoke("getScreenBrightnessTime",i, uSecNow, mStatsType) / 1000;
	            power += screenBinPower * brightnessTime;
	            if (screenBinPower * brightnessTime > 0) {
	                Log.i(TAG, "Screen bin power = " + (int) screenBinPower + ", time = " + brightnessTime);
	            }
	        }
	        power /= 1000; // To seconds
	        Log.i(TAG,"Power due to Screen Usage: "+power);
	        
	        //Add Radio Usage
	        
	        power = 0;
	        final int BINS = (Integer)ReflectionUtils.getStaticValue("android.telephony.SignalStrength","NUM_SIGNAL_STRENGTH_BINS");
	        long signalTimeMs = 0;
	        for (int i = 0; i < BINS; i++) {
	            long strengthTimeMs = (Long)mStats.invoke("getPhoneSignalStrengthTime",i, uSecNow, mStatsType) / 1000;
	            power += strengthTimeMs / 1000 * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_RADIO_ON"), i);
	            signalTimeMs += strengthTimeMs;
	        }
	        long scanningTimeMs = (Long)mStats.invoke("getPhoneSignalScanningTime",uSecNow, mStatsType) / 1000;
	        power += scanningTimeMs / 1000 * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_RADIO_SCANNING"));
	        Log.i(TAG,"Power due to Radio Usage: "+power);

	        
	        //Add Wifi Usage
			long onTimeMs = (Long)mStats.invoke("getWifiOnTime",uSecNow, mStatsType) / 1000;
        	long runningTimeMs = (Long)mStats.invoke("getGlobalWifiRunningTime",uSecNow, mStatsType) / 1000;
        	Log.v(TAG, "WIFI runningTime=" + runningTimeMs + " app runningTime=" + mAppWifiRunning);
        	runningTimeMs -= mAppWifiRunning;
        	if (runningTimeMs < 0) runningTimeMs = 0;
        	double wifiPower = (onTimeMs * 0 * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_WIFI_ON")) + runningTimeMs * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_WIFI_ON"))) / 1000;
        	Log.i(TAG,"Power due to other wifi usage : "+wifiPower);
 
        	//Add BlueTooth Usage
        	 long btOnTimeMs = (Long)mStats.invoke("getBluetoothOnTime",uSecNow, mStatsType) / 1000;
             double btPower = btOnTimeMs * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_BLUETOOTH_ON")) / 1000;
             int btPingCount = (Integer)mStats.invoke("getBluetoothPingCount",(Object []) null);
             btPower += (btPingCount * (Double)mPowerProfile.invoke("getAveragePower",mPowerProfile.getValue("POWER_BLUETOOTH_AT_CMD"))) / 1000;

	        Log.i(TAG,"Power due to Bluetooth usage"+btPower);
			
		}catch(Exception e){
			Log.e(TAG, "Error loads of them: "+e);
		}
	}
	


}
