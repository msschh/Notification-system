package com.example.ctx.fire;

import android.content.Intent;
import android.util.Log;
import android.widget.TextView;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

/**
 * Created by Costi on 5/9/2018.
 */

public class MyFirebaseMessagingService extends FirebaseMessagingService {

    public static final String TAG = "fcmexamplemessage";
    public static final String TOKEN_MESSAGE = "tokenm";

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "From: " + remoteMessage.getFrom());


        // Check if message contains a notification payload.
        if (remoteMessage.getNotification() != null) {
            Log.d(TAG, "Message Notification Body: " + remoteMessage.getNotification().getBody());
            Intent intent = new Intent(TOKEN_MESSAGE);

            String title = remoteMessage.getNotification().getTitle();
            String body  = remoteMessage.getNotification().getBody();

            intent.putExtra("title", title);
            intent.putExtra("body", body);

            getApplicationContext().sendBroadcast(intent);
        }
    }
}
