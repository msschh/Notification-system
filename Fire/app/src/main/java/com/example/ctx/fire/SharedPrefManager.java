package com.example.ctx.fire;

import android.content.Context;
import android.content.SharedPreferences;

/**
 * Created by Costi on 4/22/2018.
 */

public class SharedPrefManager {

    public static final String SHARED_PREF_NAME = "firedemo";
    private static final String KEY_ACCES_TOKEN = "token";
    private static final String KEY_ACCES_GRUPA = "grupa";

    private static Context mCtx;
    private static SharedPrefManager mInstance;

    private String grupa;

    public String getGrupa() {
        SharedPreferences sharedPreferences = mCtx.getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        return sharedPreferences.getString(KEY_ACCES_GRUPA, null);
    }

    public boolean storeGrupa(String grupa) {
        SharedPreferences sharedPreferences = mCtx.getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_ACCES_GRUPA, grupa);
        editor.apply();
        return true;
    }

    private SharedPrefManager(Context context) {
        mCtx = context;
    }

    public static synchronized SharedPrefManager getInstance(Context context) {
        if (mInstance == null)
            mInstance = new SharedPrefManager(context);
         return mInstance;
    }

    public boolean storeToken(String token) {
        SharedPreferences sharedPreferences = mCtx.getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_ACCES_TOKEN, token);
        editor.apply();
        return true;
    }

    public String getToken() {
        SharedPreferences sharedPreferences = mCtx.getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        return sharedPreferences.getString(KEY_ACCES_TOKEN, null);
    }



}
