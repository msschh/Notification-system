package com.example.ctx.fire;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    private BroadcastReceiver broadcastReceiverReceive;
    private String token;
    private String grupa;
    private BroadcastReceiver broadcastReceiverSet;
    private BroadcastReceiver broadcastReceiverMessage;

    public final String address = "93.115.17.244:11000";

    private final String TOKEN_SET = "token_set";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        grupa = SharedPrefManager.getInstance(this).getGrupa();
        final TextView textViewGroup = (TextView) findViewById(R.id.textViewGroup);
        if (grupa == null) {
            textViewGroup.setText("Nu sunteti abonat la o grupa.");
        } else {
            textViewGroup.setText("Sunteti abonat la grupa " + grupa);
        }

        broadcastReceiverMessage = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                Bundle extras = intent.getExtras();
                String title = extras.getString("title");
                String body  = extras.getString("body");

                final TextView notificationView = (TextView) findViewById(R.id.notificationView);
                notificationView.setText(title + " " + body);
            }
        };

        registerReceiver(broadcastReceiverMessage, new IntentFilter(MyFirebaseMessagingService.TOKEN_MESSAGE));

        broadcastReceiverSet = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                final Button button = findViewById(R.id.button2);
                button.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        final EditText mTextEdit = (EditText) findViewById(R.id.editText);
                        final TextView statusView = (TextView) findViewById(R.id.statusView);
                        final TextView textViewGroup = (TextView) findViewById(R.id.textViewGroup);

                        final String text = mTextEdit.getText().toString();


                        mTextEdit.setText("");

                        if (text == "") {
                            statusView.setText("Va rugam sa selectati grupa!");
                            return;
                        }

                        int nr_grupa;
                        try {
                            nr_grupa = Integer.parseInt(text);
                            if (nr_grupa < 0) {
                                statusView.setText("Introduceti un numar pozitiv");
                                return;
                            }

                        } catch (Exception e) {
                            statusView.setText("Introduceti un numar");
                            return;
                        }

                        RequestQueue queue = Volley.newRequestQueue(MainActivity.this);

                        String req = "?token="+token+"&grupa="+text;

                        //TODO: modify url to send grupa and token to our server in a post :D
                        String url ="http://" + address + "/phone" + req;
                        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                                new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String response) {
                                        statusView.setText("Ai selectat o grupa!");
                                        SharedPrefManager.getInstance(MainActivity.this).storeGrupa(text);
                                        textViewGroup.setText("Sunteti abonat la grupa " + text);
                                    }
                                }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                statusView.setText("Nu s-a putut trimite cererea: "+ error.toString());
                            }
                        });

                        queue.add(stringRequest);
                    }
                });
            }
        };

        registerReceiver(broadcastReceiverSet, new IntentFilter(TOKEN_SET));


        broadcastReceiverReceive = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                token = SharedPrefManager.getInstance(MainActivity.this).getToken();
                Log.d("token:", token);
                getApplicationContext().sendBroadcast(new Intent(TOKEN_SET));
            }
        };


        if (SharedPrefManager.getInstance(this).getToken() != null) {
            Log.d("myfcmtokenshared", SharedPrefManager.getInstance(this).getToken());
            token = SharedPrefManager.getInstance(this).getToken();
            getApplicationContext().sendBroadcast(new Intent(TOKEN_SET));
        }



        registerReceiver(broadcastReceiverReceive, new IntentFilter(MyFirebaseInstanceIdService.TOKEN_BROADCAST));
    }

}
