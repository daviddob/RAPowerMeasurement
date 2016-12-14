package edu.buffalo.tejashth.rateadaptationactivity;

import android.app.Service;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;

import android.util.Log;
import android.widget.Toast;

import java.io.File;
import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;

/**
 * Created by tejash on 4/28/16.
 */
public class BackgroundLogService extends Service {

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        this.stopSelf();
//        new FileTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);

        return super.onStartCommand(intent, flags, startId);

    }



}
