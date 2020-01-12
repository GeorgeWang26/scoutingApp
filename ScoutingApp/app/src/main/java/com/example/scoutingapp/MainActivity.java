package com.example.scoutingapp;

import android.content.Intent;
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

    boolean connected;

    String SERVER_IP = "172.17.39.164";
    int SERVER_PORT = 4264;

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

    boolean open;
    String compName;

    PrintWriter output;
    BufferedReader input;

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
                R.id.nav_home, R.id.nav_output)
                .setDrawerLayout(drawer)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);

        System.out.println(open);

        Intent intent = getIntent();
        compName = intent.getStringExtra(Main2Activity.EXTRA_MESSAGE);

        Thread1 = new Thread(new Thread1());
        Thread1.start();

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

        teamNumberField.setEnabled(false);


        Button sendButton = (Button)findViewById(R.id.button);
        sendButton.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                int RPGained = 0;
                boolean bonusRP = false;
                String result;
                String dataToSend = "POST, ";
                String teamNumber = teamNumberField.getText().toString();
                String scoredPoints = scoredPointsField.getText().toString();
                String opponentNumber = opponentNumberField.getText().toString();
                int buttonId = winGroup.getCheckedRadioButtonId();
                if(buttonId != -1 &&
                        !teamNumber.equals("") &&
                        !scoredPoints.equals("") &&
                        !opponentNumber.equals("") &&
                connected){

                    if(buttonId == winButton.getId()){
                        result = "2";
                        RPGained += 2;
                    }else if(buttonId == drawButton.getId()){
                        result = "1";
                        RPGained ++;
                    }else{
                        result = "0";
                    }

                    if(gotBonusRPBox.isChecked()){
                        bonusRP = true;
                        RPGained ++;
                    }
                    if(canClimbBox.isChecked()){
                        RPGained ++;
                    }


                    dataToSend += "teamNumber: 7476";
                    dataToSend += ", compName: " +compName;
                    dataToSend += ", scoutTeam: " +opponentNumber;
                    dataToSend += ", auto: " +canAutoBox.isChecked();
                    dataToSend += ", score: " +scoredPoints;
                    dataToSend += ", bonusRP: " +bonusRP;
                    dataToSend += ", climb: " +canClimbBox.isChecked();
                    dataToSend += ", result: " +result;
                    dataToSend += ", totalRP:" +RPGained;

                    teamNumberField.setText("7476");
                    opponentNumberField.setText("");
                    scoredPointsField.setText("");

                    canClimbBox.setChecked(false);
                    canAutoBox.setChecked(false);

                    gotClimbRPBox.setChecked(false);
                    gotBonusRPBox.setChecked(false);

                    winGroup.clearCheck();


                    new Thread(new Thread3(dataToSend)).start();


                }
                if(!connected){
                    Toast.makeText(getApplicationContext(), "Error: No connection",
                            Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    @Override
    protected void onPause(){
        super.onPause();
        System.out.println("App Suspended");
        new Thread(new Thread3("BYE")).start();
        open = false;
    }
    


    class Thread1 implements Runnable {
        public void run() {
            Socket socket;
            if(!open) return;
            try {
                socket = new Socket(SERVER_IP, SERVER_PORT);
                connected = true;
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
                connected = false;
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
            System.out.println(message);
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
