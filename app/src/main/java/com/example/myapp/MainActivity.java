package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;


import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.view.View;
import android.widget.TextView;


public class MainActivity extends AppCompatActivity {

    EditText testText1;
    EditText testText2;
    Button testButton;
    TextView testText3;
    int counter = 0;
    String test1, test2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        testText1 = (EditText)findViewById(R.id.editText3);
        testText2 = (EditText)findViewById(R.id.editText4);
        testText3 = (TextView)findViewById(R.id.textView3);
        testButton = (Button)findViewById(R.id.button);

        testText3.setVisibility(View.INVISIBLE);

        testButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                test1 = testText1.getText().toString();
                test2 = testText2.getText().toString();

                testText1.setVisibility(View.GONE);
                testText2.setVisibility(View.GONE);
                testButton.setVisibility(View.GONE);

                testText3.setVisibility(View.VISIBLE);
                testText3.setText(test1);
            }
        });
    }
}
