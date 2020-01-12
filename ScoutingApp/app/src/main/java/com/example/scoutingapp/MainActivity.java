package com.example.scoutingapp;

import android.os.Bundle;
import android.view.View;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import com.google.android.material.navigation.NavigationView;
import androidx.drawerlayout.widget.DrawerLayout;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import android.view.Menu;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    RadioGroup winGroup;

    RadioButton winButton;
    RadioButton lossButton;
    RadioButton drawButton;

    EditText teamNumberField;
    EditText scoredPointsField;

    CheckBox canClimbBox;
    CheckBox canAutoBox;

    CheckBox gotClimbRPBox;
    CheckBox gotBonusRPBox;
    CheckBox gotBonusRPBox2;

    private AppBarConfiguration mAppBarConfiguration;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        mAppBarConfiguration = new AppBarConfiguration.Builder(
                R.id.nav_home)
                .setDrawerLayout(drawer)
                .build();

        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);

        winButton = (RadioButton) findViewById(R.id.winButton);
        lossButton = (RadioButton) findViewById(R.id.lossButton);
        drawButton = (RadioButton) findViewById(R.id.drawButton);

        teamNumberField = (EditText) findViewById(R.id.teamNumberText);
        scoredPointsField = (EditText) findViewById(R.id.scoreText);

        canClimbBox = (CheckBox) findViewById(R.id.climbBox);
        canAutoBox = (CheckBox) findViewById(R.id.autoBox);

        gotClimbRPBox = (CheckBox) findViewById(R.id.climbingRPBox);
        gotBonusRPBox = (CheckBox) findViewById(R.id.bonusRPBox);
        gotBonusRPBox2 = (CheckBox) findViewById(R.id.bonusRPBox2);

        winGroup = (RadioGroup) findViewById(R.id.radioGroup);

        winGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {

            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                // find which radio button is selected
                if(checkedId == R.id.winButton) {
                    Toast.makeText(getApplicationContext(), "choice: Win",
                            Toast.LENGTH_SHORT).show();
                } else if(checkedId == R.id.lossButton) {
                    Toast.makeText(getApplicationContext(), "choice: Loss",
                            Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getApplicationContext(), "choice: Draw",
                            Toast.LENGTH_SHORT).show();
                }
            }

        });

        Button sendButton = (Button)findViewById(R.id.button);
        sendButton.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                int RPGained = 0;
                String dataToSend = "";
                String teamNumber = teamNumberField.getText().toString();
                String scoredPoints = scoredPointsField.getText().toString();
                int buttonId = winGroup.getCheckedRadioButtonId();
                if(buttonId != -1 &&
                        !teamNumber.equals("") &&
                        !scoredPoints.equals("")){

                    if(buttonId == winButton.getId()){
                        RPGained += 2;
                    }else if(buttonId == drawButton.getId()){
                        RPGained += 1;
                    }
                        
                    Toast.makeText(getApplicationContext(), "choice: Loss",
                            Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }
}
