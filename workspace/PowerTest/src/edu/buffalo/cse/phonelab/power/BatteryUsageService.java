package edu.buffalo.cse.phonelab.power;


import edu.buffalo.cse.phonelab.lib.BatteryStatsImpl;
import edu.buffalo.cse.phonelab.lib.ReflectionUtils;
import android.app.AlarmManager;
import android.app.IntentService;
import android.content.Intent;
import android.os.SystemClock;
import android.util.Log;

public class BatteryUsageService extends IntentService {

	public static final long INITIAL_DELAY_MS = 1000;
	public static final long INTERVAL = AlarmManager.INTERVAL_FIFTEEN_MINUTES;
	BatteryStatsImpl mStats;
	static String TAG = "BatteryUsageService";
	public BatteryUsageService() {
		super("BatteryUsageService");
		mStats = new BatteryStatsImpl();
		// TODO Auto-generated constructor stub
	}

	@Override
	protected void onHandleIntent(Intent intent) {
		// TODO Auto-generated method stub
		Log.v(TAG,"Service Started");
		
		try
		{
			Object mStatsType = ReflectionUtils.getStaticValue("android.os.BatteryStats", "STATS_SINCE_UNPLUGGED");
			Class mStats1 = Class.forName("com.android.internal.os.BatteryStatsImpl");
	        long uSecTime = (Long) mStats.invoke("computeBatteryRealtime",SystemClock.elapsedRealtime() * 1000, mStatsType);
			Log.i(TAG, "uSecTime = "+uSecTime);
					
	}catch(Exception e)
	{
		Log.e(TAG, e.toString());
	}
		
	/* end of method*/	

	}

}
