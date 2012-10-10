package edu.buffalo.cse.phonelab.power;
import edu.buffalo.cse.phonelab.power.BatteryAlarmReceiver;
import edu.buffalo.cse.phonelab.power.BatteryUsageService;
import android.app.AlarmManager;
import android.app.IntentService;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.SystemClock;
import android.util.Log;


public class BatteryIntentService extends IntentService {

	public BatteryIntentService() {
		super("BatteryIntentService");
		// TODO Auto-generated constructor stub
	}

	@Override
	protected void onHandleIntent(Intent intent) {
		// TODO Auto-generated method stub
		Log.v("BatteryIntentService", "Service Started");
		// TODO Auto-generated method stub
		Context context = getApplicationContext();
		AlarmManager manager = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
		PendingIntent pIntent = PendingIntent.getBroadcast(context, 0, new Intent(context, BatteryAlarmReceiver.class), PendingIntent.FLAG_UPDATE_CURRENT);		
		manager.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, SystemClock.elapsedRealtime() + BatteryUsageService.INITIAL_DELAY_MS, BatteryUsageService.INTERVAL, pIntent);
		
	}

}
