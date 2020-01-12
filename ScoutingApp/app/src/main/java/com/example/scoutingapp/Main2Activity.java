package com.example.scoutingapp;

import android.content.Intent;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;

public class Main2Activity extends AppCompatActivity {

    ImageButton dabButton;

    EditText compNameField;

    public static final String EXTRA_MESSAGE = "com.example.scoutingApp.MESSAGE";
    String compName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        compNameField = (EditText) findViewById(R.id.compNameText);

        dabButton = (ImageButton) findViewById(R.id.dabButton);

        dabButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Start your second activity
                compName = compNameField.getText().toString().toLowerCase();
                if(!compName.equals("")) {
                    Intent intent = new Intent(Main2Activity.this, MainActivity.class);
                    intent.putExtra(EXTRA_MESSAGE, compName);
                    startActivity(intent);
                }
            }
        });

    }

}
