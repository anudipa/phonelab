package edu.buffalo.cse.phonelab.power;

import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class StartActivity extends Activity {

	private Button btnStart;
	private Button btnStop;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);
        
        btnStart = (Button)findViewById(R.id.start);
        btnStop = (Button)findViewById(R.id.stop);
        final Intent myIntent = new Intent(this, TestIntentService.class);
        
        btnStart.setOnClickListener(new OnClickListener()
        {

			@Override
			public void onClick(View v) {
				Log.i("TAG", "Start Button Clicked");
				startService(myIntent);
				
			}
        	
        });
        
        btnStop.setOnClickListener(new OnClickListener()
        {

			@Override
			public void onClick(View v) {
				Log.i("TAG", "Stop Button Clicked");
				stopService(myIntent);
				
			}
        	
        });
        
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_start, menu);
        return true;
    }
}
