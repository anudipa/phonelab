package edu.buffalo.cse.phonelab.usagemonitor;

import org.json.JSONObject;

import edu.buffalo.cse.phonelab.lib.BatteryStatsImpl;
import edu.buffalo.cse.phonelab.lib.PowerProfile;
import edu.buffalo.cse.phonelab.lib.ReflectionUtils;
import android.app.IntentService;
import android.content.Intent;
import android.os.SystemClock;
import android.util.Log;


public class BatteryUsageService extends IntentService{

	BatteryStatsImpl mStats;
	static String TAG = "BatteryUsageDetails";
	double mAppWifiRunning = (double) 0.0;
	JSONObject parentjson;	
	JSONObject childjson;
	
	public BatteryUsageService() {
		super("TestIntentService");
		mStats = new BatteryStatsImpl();
	}
	
	@Override
	protected void onHandleIntent(Intent intent) {
		Log.v(TAG,"Service Started");
		
		try
		{
			Object mStatsType = ReflectionUtils.getStaticValue("android.os.BatteryStats", "STATS_SINCE_UNPLUGGED");
			
	        long uSecTime = (Long) mStats.invoke("computeBatteryRealtime",SystemClock.elapsedRealtime() * 1000, mStatsType);
			Log.i(TAG, "uSecTime = "+uSecTime);
			//createParentJson();
			//calculateAppPower((Integer)mStatsType,uSecTime);
			//calculateMiscPower((Integer)mStatsType,uSecTime);	
	
		
	}catch(Exception e)
	{
		Log.e(TAG, e.toString());
	}
		
	/* end of method*/	
	}
	
	/*
	 * AverageCost Per Byte Calculation
	 */
	public double getAverageCostPerByte(int mStatsType)
	{
		PowerProfile mPowerProfile = new PowerProfile(getApplicationContext());
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
			if (wifiData + mobileData != 0) 
				{
					return (mobileCostPerByte * mobileData + wifiCostPerByte * wifiData) / (mobileData + wifiData);
				} 
//			Log.v(TAG, WIFI_POWER+" , "+MOBILE_POWER+"  ,  "+mobileData+"  ,  "+wifiData);
//			Log.v(TAG, "The average Data cost is "+averageCostPerByte);
		}catch(Exception e)
		{
			Log.e(TAG, "Error @ averageCostPerByte "+e);
		}
		return 0.0;
		
	}
	
	
	
	
}