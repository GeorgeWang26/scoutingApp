package com.example.scoutingapp.ui.home;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.scoutingapp.R;

public class OutputFragment extends Fragment {

    private OutputViewModel outputViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater,
            ViewGroup container, Bundle savedInstanceState) {
        outputViewModel =
                ViewModelProviders.of(this).get(OutputViewModel.class);
        View root = inflater.inflate(R.layout.fragment_output, container, false);
        final TextView textView = root.findViewById(R.id.output);
        outputViewModel.getText().observe(this, new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }
}