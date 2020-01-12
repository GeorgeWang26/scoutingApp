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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    Socket socket;

    String SERVER_IP = "172.17.39.164";
    int SERVER_PORT = 4258;

    PrintWriter out;
    BufferedReader in;

    Thread Thread1 = null;

    RadioGroup winGroup;

    RadioButton winButton;
    RadioButton lossButton;
    RadioButton drawButton;

    EditText teamNumberField;
    EditText scoredPointsField;
    EditText opponentNumberField;

    CheckBox canClimbBox;
    CheckBox canAutoBox;

    CheckBox gotClimbRPBox;
    CheckBox gotBonusRPBox;

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
        opponentNumberField = (EditText) findViewById(R.id.opponentNumberText);

        canClimbBox = (CheckBox) findViewById(R.id.climbBox);
        canAutoBox = (CheckBox) findViewById(R.id.autoBox);

        gotClimbRPBox = (CheckBox) findViewById(R.id.climbingRPBox);
        gotBonusRPBox = (CheckBox) findViewById(R.id.bonusRPBox);

        winGroup = (RadioGroup) findViewById(R.id.radioGroup);

        Thread1 = new Thread(new Thread1());
        Thread1.start();
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
                int bonusRP = 0;
                String result;
                String dataToSend = "POST, ";
                String teamNumber = teamNumberField.getText().toString();
                String scoredPoints = scoredPointsField.getText().toString();
                String opponentNumber = opponentNumberField.getText().toString();
                int buttonId = winGroup.getCheckedRadioButtonId();
                if(buttonId != -1 &&
                        !teamNumber.equals("") &&
                        !scoredPoints.equals("") &&
                        !opponentNumber.equals("")){

                    if(buttonId == winButton.getId()){
                        result = "2";
                        RPGained += 2;
                    }else if(buttonId == drawButton.getId()){
                        result = "1";
                        RPGained ++;
                    }else{
                        result = "0";
                    }

                    if(gotClimbRPBox.isChecked()){
                        bonusRP++;
                    }
                    if(gotBonusRPBox.isChecked()){
                        bonusRP++;
                    }

                    RPGained += bonusRP;

                    dataToSend += "teamNumber: 7476";
                    dataToSend += ", compName: Carleton";
                    dataToSend += ", scoutTeam: " +opponentNumber;
                    dataToSend += ", auto: " +canAutoBox.isChecked();
                    dataToSend += ", score: " +scoredPoints;
                    dataToSend += ", climb: " +canClimbBox.isChecked();
                    dataToSend += ", bonusRP: " +bonusRP;
                    dataToSend += ", result: " +result;
                    dataToSend += ", totalRP:" +RPGained;

                    teamNumberField.setText("7476");
                    opponentNumberField.setText("");
                    scoredPointsField.setText("0");

                    canClimbBox.setSelected(false);
                    canAutoBox.setSelected(false);

                    gotClimbRPBox.setSelected(false);
                    gotBonusRPBox.setSelected(false);

                    winGroup.clearCheck();

                    new Thread(new Thread3(dataToSend)).start();

                }
            }
        });
    }

    private PrintWriter output;
    private BufferedReader input;
    class Thread1 implements Runnable {
        public void run() {
            Socket socket;
            try {
                socket = new Socket(SERVER_IP, SERVER_PORT);
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                    }
                });
                new Thread(new Thread2()).start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    class Thread2 implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {
                    final String message = input.readLine();
                    if (message != null) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {

                            }
                        });
                    } else {
                        Thread1 = new Thread(new Thread1());
                        Thread1.start();
                        return;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    class Thread3 implements Runnable {
        private String message;
        Thread3(String message) {
            this.message = message;
        }
        @Override
        public void run() {
            output.write(message);
            output.flush();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {

                }
            });
        }
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }


    public void listenSocket(){
//Create socket connection
        try{
            socket = new Socket("172.17.39.164", 4258);
            out = new PrintWriter(socket.getOutputStream(),
                    true);
            in = new BufferedReader(new InputStreamReader(
                    socket.getInputStream()));
        } catch (UnknownHostException e) {
            Toast.makeText(getApplicationContext(), "Unknown Host: 172.17.39.164",
                    Toast.LENGTH_SHORT).show();
        } catch  (IOException e) {
            Toast.makeText(getApplicationContext(), "No I/O",
                    Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }
}
