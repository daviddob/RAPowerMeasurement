package edu.buffalo.tejashth.rateadaptationactivity;

/*Created By Tejeet Desai*/


import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.StringTokenizer;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends Activity {

    final float[] coreValues = new float[10];   //array to store each core's utilization
    static boolean finish = false;
    int zeroes = 0; // used to know if any of the core's utilization is zero i.e. it is not in use
    double pbase = 0.0;  // applied in formula from hotpower paper
    double pdelta = 0.0; // applied in formula from hotpower paper
    double pcpu = 0.0;  // applied in formula from hotpower paper

    private static final String MCS0 = "mcs0";
    private static final String MCS1 = "mcs1";
    private static final String MCS2 = "mcs2";
    private static final String MCS3 = "mcs3";
    private static final String MCS4 = "mcs4";
    private static final String MCS5 = "mcs5";
    private static final String MCS6 = "mcs6";
    private static final String MCS7 = "mcs7";
    private static final String MCS8 = "mcs8";
    private static final String MCS9 = "mcs9";
    private static final String MCS10 = "mcs10";
    private static final String MCS11 = "mcs11";
    private static final String MCS12 = "mcs12";
    private static final String MCS13 = "mcs13";
    private static final String MCS14 = "mcs14";
    private static final String MCS15 = "mcs15";
    private static final String MCSRA = "mcsra";
    public static final String F20MHz = "20MHz";
    public static final String F40MHz = "40MHz";
    private static final String Location1 = "Location1";
    private static final String Location2 = "Location2";
    private static final String Location3 = "Location3";
    private static final String Location4 = "Location4";
    private static final String Location5 = "Location5";
    private static final String Location6 = "Location6";
    private static final String Location7 = "Location7";
    private static final String Location8 = "Location8";
    public static final String FREQ = "Freq";
    public String iperfFile;
    int reading = 1;
    private String readingsDirectory;
    private static final String SLASH = "/";
    private static final String UNDERSCORE = "_";

    private static final HashMap<String, Integer> limit20MHzHash = new HashMap<>();
    private static final HashMap<String, Integer> limit40MHzHash = new HashMap<>();

    private static final String MBPS = "mbps";
    private static final int[] arrDataRates20MHz = new int[]{2, 8, 15, 22, 35, 45, 53, 60, 4, 16, 30, 44, 70, 90, 106, 120};
    private static final int[] arrDataRates40MHz = new int[]{5, 20, 30, 40, 65, 80, 90, 100, 10, 40, 60, 80, 130, 160, 180, 200};
    private static final int TOTAL_READINGS = 5;
    private int currentDataRate = 0;
    private TextView mTxtInfo;
    private String selectedFreq = F20MHz;
    private String selectedLocation = Location1;
    private FileTask fileTask;
    private boolean started;

    String[] arrMCS = new String[]{MCS0, MCS1, MCS2, MCS3, MCS4, MCS5, MCS6, MCS7, MCS8,
            MCS9, MCS10, MCS11, MCS12, MCS13, MCS14, MCS15, MCSRA};

    HashMap<Integer, Double> core1d = new HashMap<>();  // used to store each core's pdelta value for each frequency
    HashMap<Integer, Double> core2d = new HashMap<>();
    HashMap<Integer, Double> core3d = new HashMap<>();
    HashMap<Integer, Double> core4d = new HashMap<>();
    HashMap<Integer, Double> core1b = new HashMap<>();  // used to store each core's pbase value for each frequency
    HashMap<Integer, Double> core2b = new HashMap<>();
    HashMap<Integer, Double> core3b = new HashMap<>();
    HashMap<Integer, Double> core4b = new HashMap<>();


    Timer timer;
    TimerTask timerTask;
    TimerTask fileTimerTask;
    Timer fileTimer;
    //we are going to use a handler to be able to run in our TimerTask
    final Handler handler = new Handler();
    final Handler fileHandler = new Handler();
    IperfTask iperfTask = null;

    public void startTimer() {

        Log.d("Starting timer task", "Starting timer");
        //set a new Timer
        timer = new Timer();

        //initialize the TimerTask's job
        initializeTimerTask();

        //schedule the timer, after the first 5000ms the TimerTask will run every 10000ms
        timer.schedule(timerTask, 4500, 18000); //
    }

    public void startFileTimer() {

        Log.d("Starting timer task", "Starting timer");
        //set a new Timer
        fileTimer = new Timer();

        //initialize the TimerTask's job
        initializeFileTimerTask();

        //schedule the timer, after the first 5000ms the TimerTask will run every 10000ms
        fileTimer.schedule(fileTimerTask, 500, 18000); //
    }


    public void setTextView(){
        String str = selectedLocation + " " + arrMCS[mcsIndex]+" datarate:"+ (selectedFreq.equals(F20MHz) ? arrDataRates20MHz[datarateIndex]
                : arrDataRates40MHz[datarateIndex]) +" reading:"+reading;
        mTxtInfo.setText(str);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        started = false;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        iperfFile = MainActivity.this.getFilesDir() + "/iperf";
        Log.d("iperfFile", iperfFile);
        mTxtInfo = (TextView) findViewById(R.id.txtInfo);
        setTextView();
//        Log.d("OnstartCommand", "On start");
//        Toast.makeText(this, "start service", Toast.LENGTH_SHORT).show();
        initializeCoreValues();
        readingsDirectory = this.getFilesDir().getAbsolutePath();

        limit20MHzHash.put(MCS0, 7);
        limit20MHzHash.put(MCS1, 13);
        limit20MHzHash.put(MCS2, 20);
        limit20MHzHash.put(MCS3, 26);
        limit20MHzHash.put(MCS4, 39);
        limit20MHzHash.put(MCS5, 52);
        limit20MHzHash.put(MCS6, 59);
        limit20MHzHash.put(MCS7, 65);
        limit20MHzHash.put(MCS8, 13);
        limit20MHzHash.put(MCS9, 26);
        limit20MHzHash.put(MCS10, 39);
        limit20MHzHash.put(MCS11, 52);
        limit20MHzHash.put(MCS12, 78);
        limit20MHzHash.put(MCS13, 104);
        limit20MHzHash.put(MCS14, 117);
        limit20MHzHash.put(MCS15, 130);
        limit20MHzHash.put(MCSRA, 130);
        
        limit40MHzHash.put(MCS0, 14);
        limit40MHzHash.put(MCS1, 27);
        limit40MHzHash.put(MCS2, 35);
        limit40MHzHash.put(MCS3, 54);
        limit40MHzHash.put(MCS4, 75);
        limit40MHzHash.put(MCS5, 85);
        limit40MHzHash.put(MCS6, 95);
        limit40MHzHash.put(MCS7, 105);
        limit40MHzHash.put(MCS8, 28);
        limit40MHzHash.put(MCS9, 54);
        limit40MHzHash.put(MCS10, 70);
        limit40MHzHash.put(MCS11, 108);
        limit40MHzHash.put(MCS12, 150);
        limit40MHzHash.put(MCS13, 170);
        limit40MHzHash.put(MCS14, 190);
        limit40MHzHash.put(MCS15, 210);
        limit40MHzHash.put(MCSRA, 210);

        // Initializing values obtained from cpu model for S4

//        final Button b1 = (Button) findViewById(R.id.button20);
//        final Button b2 = (Button) findViewById(R.id.button40);
//        final Button b3 = (Button) findViewById(R.id.buttonMCS);
        final Button start = (Button) findViewById(R.id.start_logging);
        final Button b4 = (Button) findViewById(R.id.buttonDatarate);

        Spinner locationSpinner = (Spinner) findViewById(R.id.dropdown_location);
        ArrayAdapter<CharSequence> locationAdapter = ArrayAdapter.createFromResource(this,
                R.array.locations_array, android.R.layout.simple_spinner_item);
        locationAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        locationSpinner.setAdapter(locationAdapter);

        Spinner mcsSpinner = (Spinner) findViewById(R.id.dropdown_mcs);
        ArrayAdapter<CharSequence> mcsAdapter = ArrayAdapter.createFromResource(this,
                R.array.mcs_array, android.R.layout.simple_spinner_item);
        mcsAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        mcsSpinner.setAdapter(mcsAdapter);

        Spinner freqSpinner = (Spinner) findViewById(R.id.dropdown_freq);
        ArrayAdapter<CharSequence> freqAdapter = ArrayAdapter.createFromResource(this,
                R.array.freq_array, android.R.layout.simple_spinner_item);
        freqAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        freqSpinner.setAdapter(freqAdapter);

        final MainActivity self = this;

        if(start != null){
            start.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if(!started){
                        started = true;
                        startProcess();
                        Toast.makeText(self, "Start service", Toast.LENGTH_SHORT).show();
                    }
                    else{
                        Toast.makeText(self, "Already started", Toast.LENGTH_SHORT).show();

                    }

                }
            });
        }
        if (b4!= null) {
            b4.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    datarateIndex = ++datarateIndex % arrDataRates40MHz.length;
                    setTextView();
                }
            });
        }



        if(locationSpinner != null){
            locationSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                    selectedLocation = (String) adapterView.getItemAtPosition(i);
                    setTextView();
                }

                @Override
                public void onNothingSelected(AdapterView<?> adapterView) {
                    selectedLocation = (String) adapterView.getItemAtPosition(0);
                }
            });
        }

        if(mcsSpinner != null){
            mcsSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){

                @Override
                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                    mcsIndex = i;
                    setTextView();
                }

                @Override
                public void onNothingSelected(AdapterView<?> adapterView) {
                    mcsIndex = 0;
                }
            });
        }

        if(freqAdapter != null){
            freqSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                    selectedFreq = (String) adapterView.getItemAtPosition(i);
                    setTextView();
                }

                @Override
                public void onNothingSelected(AdapterView<?> adapterView) {
                    selectedFreq = (String) adapterView.getItemAtPosition(0);
                }
            });
        }

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
    }

    public void startProcess() {


        new CoreTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);  // calculates each core's utilization
        startTimer();
        startFileTimer();


    }

    public void changePermission(){
        Process processChmod = null;
        Log.d("Hey, I am starting","Yey");
        String strFileName = this.getFilesDir().getAbsolutePath()+SLASH+"test";
        try {
            Log.d("filname",strFileName);
            processChmod = Runtime.getRuntime().exec("su -c /system/bin/chmod 777 -R "+strFileName);
            processChmod.waitFor();

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        // Executes the command and waits untill it finishes.
    }

    private boolean runNextTimeTemp = true;
    public void initializeTimerTask() {

        timerTask = new TimerTask() {
            @Override
            public void run() {

                //use a handler to run a toast that shows the current timestamp
                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        Log.d("Starting iperf", "Yey");
                        //get the current timeStamp
                        if(!runNextTimeTemp){
                            timer.cancel();
                            timerTask.cancel();
                            return;
                        }
                        if(!runNextTime){
                            runNextTimeTemp= false;
                        }

                        initIperf();
                    }
                });

            }
        };
    }

    public void initializeFileTimerTask() {

        fileTimerTask = new TimerTask() {
            @Override
            public void run() {

                //use a handler to run a toast that shows the current timestamp
                fileHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        setTextView();
                        Log.d("Logging", "Logging");
//                        fileHandler.postDelayed(tt, 18000);
                        String strMCS = arrMCS[mcsIndex];
                        int dataRate = (selectedFreq.equals(F20MHz)) ? arrDataRates20MHz[datarateIndex]
                                : arrDataRates40MHz[datarateIndex];
                        currentDataRate = dataRate;
                        int maxDataRate;
                        if (selectedFreq.equals(F20MHz)) {
                            maxDataRate = limit20MHzHash.get(strMCS);
                        } else {
                            maxDataRate = limit40MHzHash.get(strMCS);
                        }
                        File file = new File(readingsDirectory + SLASH + selectedFreq + SLASH + selectedLocation + SLASH+ strMCS + SLASH + dataRate + MBPS + SLASH + reading);
                        file.mkdirs();
                        String strFileName = selectedFreq + UNDERSCORE + strMCS + dataRate + MBPS + UNDERSCORE + reading;
                        Log.d("File Name", strFileName);
                        File outputFile = new File(file, strFileName);
                        Log.d("File Path", outputFile.getAbsolutePath() + "::" + outputFile.getAbsolutePath());
                        if (!runNextTime) {
//                            fileHandler.removeCallbacks(tt);
//                            fileTimer.cancel();
//                            fileTimerTask.cancel();
//                            timerTask.cancel();
//                            timer.cancel();

                            return;

                        }

                        new FileTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, outputFile);

//                writeToFile(outputFile);
//                if(runNextTime)
                        reading++;
                        if (reading == TOTAL_READINGS+1) {
                            reading = 1;

                            datarateIndex++;
                            if ((selectedFreq.equals(F20MHz) &&
                                    (datarateIndex == arrDataRates20MHz.length || arrDataRates20MHz[datarateIndex] > maxDataRate))
                                    || (selectedFreq.equals(F40MHz) &&
                                    (datarateIndex == arrDataRates40MHz.length || arrDataRates40MHz[datarateIndex] > maxDataRate))
                                    ) {
                                datarateIndex = 0;
                                runNextTime = false;
                                fileTimer.cancel();
                                fileTimerTask.cancel();
                            }





//                                timerTask.cancel();
//                                timer.cancel();

//                        mcsIndex++;
//                        if (mcsIndex == arrMCS.length - 1) {
//                            if (tt != null) {
//                                tt.cancel();
//                                finish = true;
//                            }
//                        }
                        }


                        /// write coding for your requirement here
                    }
                });

            }
        };
    }

    private int mcsIndex = 0;
    private int datarateIndex = 0;
    TimerTask tt;
    boolean runNextTime = true;


    @Override
    public void onStart() {
        super.onStart();

    }

    @Override
    public void onStop() {
        super.onStop();

    }


    private class CoreTask extends AsyncTask<String, Void, Void> {


        @Override
        protected Void doInBackground(String... msgs) {


            while (!finish) {
                readCore();
            }
            return null;
        }
    }


    public void initializeCoreValues() {
        core1d.put(250000, 98.916);
        core1d.put(300000, 112.914);
        core1d.put(350000, 122.068);
        core1d.put(400000, 140.754);
        core1d.put(450000, 185.69);
        core1d.put(500000, 203.144);
        core1d.put(550000, 242.674);
        core1d.put(600000, 260.47);
        core1d.put(800000, 414.8805);
        core1d.put(900000, 501.128);
        core1d.put(1000000, 627.848);
        core1d.put(1100000, 721.372);
        core1d.put(1200000, 860.934);
        core1d.put(1300000, 1025.2);
        core1d.put(1400000, 1209.59);
        core1d.put(1500000, 1412.7);
        core1d.put(1600000, 1644.2);

        core2d.put(250000, 73.25);
        core2d.put(300000, 82.04);
        core2d.put(350000, 91.776);
        core2d.put(400000, 108.544);
        core2d.put(450000, 131.847);
        core2d.put(500000, 153.189);
        core2d.put(550000, 167.922);
        core2d.put(600000, 196.598);
        core2d.put(800000, 389.577);
        core2d.put(900000, 466.293);
        core2d.put(1000000, 574.99);
        core2d.put(1100000, 683.288);
        core2d.put(1200000, 814.033);
        core2d.put(1300000, 1039.42);
        core2d.put(1400000, 1269.48);
        core2d.put(1500000, 1540.00);
        core2d.put(1600000, 1862.24);

        core3d.put(250000, 62.186);
        core3d.put(300000, 72.172);
        core3d.put(350000, 76.15733);
        core3d.put(400000, 79.314);
        core3d.put(450000, 116.9187);
        core3d.put(500000, 155.5667);
        core3d.put(550000, 163.7353);
        core3d.put(600000, 190.9933);
        core3d.put(800000, 388.2897);
        core3d.put(900000, 467.3667);
        core3d.put(1000000, 585.3687);
        core3d.put(1100000, 700.2853);
        core3d.put(1200000, 838.0933);
        core3d.put(1300000, 1140.63);
        core3d.put(1400000, 1428.71);
        core3d.put(1500000, 1782.13);
        core3d.put(1600000, 2216.58);

        core4d.put(250000, 51.776);
        core4d.put(300000, 58.5505);
        core4d.put(350000, 71.2435);
        core4d.put(400000, 62.1025);
        core4d.put(450000, 117.4105);
        core4d.put(500000, 117.142);
        core4d.put(550000, 155.8265);
        core4d.put(600000, 195.074);
        core4d.put(800000, 389.3873);
        core4d.put(900000, 476.7625);
        core4d.put(1000000, 605.2075);
        core4d.put(1100000, 739.1955);
        core4d.put(1200000, 905.5035);
        core4d.put(1300000, 1283.65);
        core4d.put(1400000, 1653.25);
        core4d.put(1500000, 2121.68);
        core4d.put(1600000, 2716.01);

        core1b.put(250000, 272.474);
        core1b.put(300000, 271.104);
        core1b.put(350000, 274.074);
        core1b.put(400000, 276.638);
        core1b.put(450000, 280.316);
        core1b.put(500000, 282.734);
        core1b.put(550000, 289.026);
        core1b.put(600000, 296.642);
        core1b.put(800000, 316.312);
        core1b.put(900000, 316.654);
        core1b.put(1000000, 320.892);
        core1b.put(1100000, 330.632);
        core1b.put(1200000, 330.446);
        core1b.put(1300000, 341.114);
        core1b.put(1400000, 342.658);
        core1b.put(1500000, 350.784);
        core1b.put(1600000, 359.274);

        core2b.put(250000, 271.842);
        core2b.put(300000, 272.486);
        core2b.put(350000, 274.464);
        core2b.put(400000, 278.324);
        core2b.put(450000, 282.288);
        core2b.put(500000, 286.15);
        core2b.put(550000, 293.666);
        core2b.put(600000, 303.81);
        core2b.put(800000, 322.694);
        core2b.put(900000, 326.832);
        core2b.put(1000000, 333.566);
        core2b.put(1100000, 346.04);
        core2b.put(1200000, 349.764);
        core2b.put(1300000, 362.114);
        core2b.put(1400000, 366.076);
        core2b.put(1500000, 377.378);
        core2b.put(1600000, 390.258);

        core3b.put(250000, 271.53);
        core3b.put(300000, 272.03);
        core3b.put(350000, 274.438);
        core3b.put(400000, 278.472);
        core3b.put(450000, 282.458);
        core3b.put(500000, 286.534);
        core3b.put(550000, 294.028);
        core3b.put(600000, 303.726);
        core3b.put(800000, 324.194);
        core3b.put(900000, 327.012);
        core3b.put(1000000, 334.242);
        core3b.put(1100000, 345.538);
        core3b.put(1200000, 350.918);
        core3b.put(1300000, 360.046);
        core3b.put(1400000, 367.052);
        core3b.put(1500000, 378.732);
        core3b.put(1600000, 394.278);

        core4b.put(250000, 271.852);
        core4b.put(300000, 272.26);
        core4b.put(350000, 274.784);
        core4b.put(400000, 278.71);
        core4b.put(450000, 282.206);
        core4b.put(500000, 297.424);
        core4b.put(550000, 293.92);
        core4b.put(600000, 304.218);
        core4b.put(800000, 324.376);
        core4b.put(900000, 327.394);
        core4b.put(1000000, 334.408);
        core4b.put(1100000, 345.854);
        core4b.put(1200000, 350.49);
        core4b.put(1300000, 360.96);
        core4b.put(1400000, 366.768);
        core4b.put(1500000, 378.084);
        core4b.put(1600000, 394.934);

    }

    //for multi core value
    private void readCore() {
            /*
             * how to calculate multicore
             * this function reads the bytes from a logging file in the android system (/proc/stat for cpu values)
             * then puts the line into a string
             * then spilts up each individual part into an array
             * then(since he know which part represents what) we are able to determine each cpu total and work
             * then combine it together to get a single float for overall cpu usage
             */
        long work1[] = new long[5];
        long total1[] = new long[5];
        long work2[] = new long[5];
        long total2[] = new long[5];
        try {
            RandomAccessFile reader = new RandomAccessFile("/proc/stat", "r");
            //skip to the line we need

            reader.readLine();
            for (int i1 = 0; i1 < 4; i1++) {
                String load = reader.readLine();

                //cores will eventually go offline, and if it does, then it is at 0% because it is not being
                //used. so we need to do check if the line we got contains cpu, if not, then this core = 0
                if (load.contains("cpu")) {
                    String[] toks = load.split(" ");

                    //we are recording the work being used by the user and system(work) and the total info
                    //of cpu stuff (total)
                    //http://stackoverflow.com/questions/3017162/how-to-get-total-cpu-usage-in-linux-c/3017438#3017438

                    work1[i1] = Long.parseLong(toks[1]) + Long.parseLong(toks[2]) + Long.parseLong(toks[3]);
                    total1[i1] = Long.parseLong(toks[1]) + Long.parseLong(toks[2]) + Long.parseLong(toks[3]) +
                            Long.parseLong(toks[4]) + Long.parseLong(toks[5])
                            + Long.parseLong(toks[6]) + Long.parseLong(toks[7]) + Long.parseLong(toks[8]);
                } else {
                    reader.close();
                    coreValues[i1] = 0;
                }
            }


            try {
                Thread.sleep(100);
            } catch (Exception e) {
            }

            reader.seek(0);
            //skip to the line we need
            reader.readLine();

            for (int i2 = 0; i2 < 4; i2++) {

                String load = reader.readLine();
                //cores will eventually go offline, and if it does, then it is at 0% because it is not being
                //used. so we need to do check if the line we got contains cpu, if not, then this core = 0%
                if (load.contains("cpu")) {
                    String[] toks = load.split(" ");

                    work2[i2] = Long.parseLong(toks[1]) + Long.parseLong(toks[2]) + Long.parseLong(toks[3]);
                    total2[i2] = Long.parseLong(toks[1]) + Long.parseLong(toks[2]) + Long.parseLong(toks[3]) +
                            Long.parseLong(toks[4]) + Long.parseLong(toks[5])
                            + Long.parseLong(toks[6]) + Long.parseLong(toks[7]) + Long.parseLong(toks[8]);


                    //here we find the change in user work and total info, and divide by one another to get our total
                    //http://stackoverflow.com/questions/3017162/how-to-get-total-cpu-usage-in-linux-c/3017438#3017438

                    if ((total2[i2] - total1[i2]) == 0)
                        coreValues[i2] = 0;
                    else
                        coreValues[i2] = (float) (work2[i2] - work1[i2]) * 100 / ((total2[i2] - total1[i2]));
                } else {
                    reader.close();
                    coreValues[i2] = 0;
                }
            }
            reader.close();
        } catch (IOException ex) {
            ex.printStackTrace();
        }

    }

    private class FileTask extends AsyncTask<File, Void, Void> {

        @Override
        protected Void doInBackground(File... params) {
            writeToFile(params[0]);
            return null;
        }
    }

    public void writeToFile(File outputFile) {
        int frequency; //variable to store frequency value
        String output;  // final output to be written to a file
        String timestamp;   // variable to store timestamp
        FileOutputStream fos = null;
        String filename;
        int reading_number = 0; //variable to store number of logs in logfile

        try {
            fos = new FileOutputStream(outputFile);
        } catch (Exception e) {
            Log.e("open", "failed");
        }

        for (int j = 0; j <= 18000; ) {       //running for 18 secs, to account for time taken to start core utilization and iperf

            zeroes = 0;

            frequency = readFrequency();
            timestamp = getTimestamp();

            output = timestamp + " " + Integer.toString(frequency) + " " + Float.toString(coreValues[0]) + " " + Float.toString(coreValues[1]) + " " + Float.toString(coreValues[2]) + " " + Float.toString(coreValues[3]) + "\n";
            try {
                fos.write(output.getBytes());
                //       fos.close();
                //       Log.v("insert", "file write success");
            } catch (Exception e) {
                Log.e("insert", "file write failed");
            }

            //           if(frequency > 1200000)
            //               frequency = 1200000;

//            for (int k = 0; k < 4; k++) {
//                if (coreValues[k] == 0.0)
//                    zeroes++;
//            }
//
//            if (zeroes == 4) {                  //when all core's utilization is 0, pcu=pbase;
//                pbase = core4b.get(frequency);
//                pcpu += pbase;
//            } else if (zeroes == 3) {           // when three core's utilization is 0, cpu values for 1 core active is taken
//                pbase = core1b.get(frequency);
//                pdelta = core1d.get(frequency);
//                pcpu += pbase + (coreValues[0] * pdelta + coreValues[1] * pdelta + coreValues[2] * pdelta + coreValues[3] * pdelta) / 100;
//            } else if (zeroes == 2) {           // when two core's utilization is 0, cpu values for 2 cores active is taken
//                pbase = core2b.get(frequency);
//                pdelta = core2d.get(frequency);
//                pcpu += pbase + (coreValues[0] * pdelta + coreValues[1] * pdelta + coreValues[2] * pdelta + coreValues[3] * pdelta) / 100;
//            } else if (zeroes == 1) {           // when one core's utilization is 0, cpu values for 3 cores active is taken
//                pbase = core3b.get(frequency);
//                pdelta = core3d.get(frequency);
//                pcpu += pbase + (coreValues[0] * pdelta + coreValues[1] * pdelta + coreValues[2] * pdelta + coreValues[3] * pdelta) / 100;
//            } else if (zeroes == 0) {           // when none core's utilization is 0, cpu values for all cores active is taken
//                Log.d("Freq", Integer.toString(frequency));
//                pbase = core4b.get(frequency);
//                pdelta = core4d.get(frequency);
//                pcpu += pbase + (coreValues[0] * pdelta + coreValues[1] * pdelta + coreValues[2] * pdelta + coreValues[3] * pdelta) / 100;
//            }
//
//            reading_number++;
//
//            output = Double.toString(pcpu) + " " + Integer.toString(reading_number) + "\n";
//            try {
//                fos.write(output.getBytes());       // write current total pcpu value and number of readings
//                //       fos.close();
//                //       Log.v("insert", "file write success");
//            } catch (Exception e) {
//                Log.e("insert", "file write failed");
//            }


            try {
                Thread.sleep(100);
            } catch (Exception e) {
                Log.e("sleep", "error");
            }

            j += 100;

        }
        try {
            fos.close();
        } catch (Exception e) {
            Log.e("insert", "file write failed");
        }

//        finish = true;

    }

    private String getTimestamp() {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date());      //get timestamp from simple date fprmat class
    }

    private int readFrequency() {
        int freq;
        try {
            RandomAccessFile reader = new RandomAccessFile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r");   //scaling_cur_freq is the file which has current cpu freq
            freq = Integer.parseInt(reader.readLine());
            reader.close();
            return freq;
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        return 0;
    }

    //This function is used to copy the iperf executable to a directory which execute permissions for this application, and then gives it execute permissions.
    //It runs on every initiation of an iperf test, but copies the file only if it's needed.
    public void initIperf() {
        Log.d("Starting iperf,", "Starting iperf");
//        final TextView tv = (TextView) findViewById(R.id.OutputText);
        InputStream in;
        try {
            //The asset "iperf" (from assets folder) inside the activity is opened for reading.
            in = getResources().getAssets().open("iperf");
        } catch (IOException e2) {
            e2.printStackTrace();
            Toast.makeText(MainActivity.this, "\nError occurred while accessing system resources, please reboot and try again.", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            //Checks if the file already exists, if not copies it.
            new FileInputStream(iperfFile);
        } catch (FileNotFoundException e1) {
            e1.printStackTrace();
            try {
                //The file named "iperf" is created in a system designated folder for this application.
                OutputStream out = new FileOutputStream(iperfFile, false);
                // Transfer bytes from "in" to "out"
                byte[] buf = new byte[1024];
                int len;
                while ((len = in.read(buf)) > 0) {
                    out.write(buf, 0, len);
                }
                in.close();
                out.close();
                //After the copy operation is finished, we give execute permissions to the "iperf" executable using shell commands.
                Process processChmod = Runtime.getRuntime().exec("/system/bin/chmod 744 " + iperfFile);
                // Executes the command and waits untill it finishes.
                processChmod.waitFor();
            } catch (IOException e) {
                e.printStackTrace();
                return;
            } catch (InterruptedException e) {
                e.printStackTrace();
                return;
            }
            String str = "-c 10.0.0.10 -u -b " + currentDataRate + "M";
            //Creates an instance of the class IperfTask for running an iperf test, then executes.
            iperfTask = new IperfTask();
            iperfTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, str);
            return;
        }
        //Creates an instance of the class IperfTask for running an iperf test, then executes.
        String str = "-c 10.0.0.10 -u -b " + currentDataRate + "M";
        iperfTask = new IperfTask();
        iperfTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, str);
        return;
    }


    //The main class for executing iperf instances.
    //With every test started, an instance of this class is created, and is destroyed when the test is done.
    //This class extends the class AsyncTask which is used to perform long background tasks and allow updates to the GUI while running.
    //This is done by overriding certain functions that offer this functionality.
    class IperfTask extends AsyncTask<String, String, String> {
//        final TextView tv = (TextView) findViewById(R.id.OutputText);
//        final ScrollView scroller = (ScrollView) findViewById(R.id.Scroller);
//        final EditText inputCommands = (EditText) findViewById(R.id.InputCommands);
//        final ToggleButton toggleButton = (ToggleButton) findViewById(R.id.toggleButton);

        Process process = null;

        //This function is used to implement the main task that runs on the background.
        @Override
        protected String doInBackground(String... strings) {
            Log.d("starting iperf", "Starting iperf");
            Log.d("iperf log", strings[0]);
            //Iperf command syntax check using a Regular expression to protect the system from user exploitation.
            String str = strings[0];
            if (!str.matches("(iperf )?((-[s,-server])|(-[c,-client] ([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(-[c,-client] \\w{1,63})|(-[h,-help]))(( -[f,-format] [bBkKmMgG])|(\\s)|( -[l,-len] \\d{1,5}[KM])|( -[B,-bind] \\w{1,63})|( -[r,-tradeoff])|( -[v,-version])|( -[N,-nodelay])|( -[T,-ttl] \\d{1,8})|( -[U,-single_udp])|( -[d,-dualtest])|( -[w,-window] \\d{1,5}[KM])|( -[n,-num] \\d{1,10}[KM])|( -[p,-port] \\d{1,5})|( -[L,-listenport] \\d{1,5})|( -[t,-time] \\d{1,8})|( -[i,-interval] \\d{1,4})|( -[u,-udp])|( -[b,-bandwidth] \\d{1,20}[bBkKmMgG])|( -[m,-print_mss])|( -[P,-parallel] d{1,2})|( -[M,-mss] d{1,20}))*")) {
                publishProgress("Error: invalid syntax. Please try again.\n\n");
                return null;
            }
            try {
                //The user input for the parameters is parsed into a string list as required from the ProcessBuilder Class.
                String[] commands = strings[0].split(" ");
                List<String> commandList = new ArrayList<String>(Arrays.asList(commands));
                //If the first parameter is "iperf", it is removed
                if (commandList.get(0).equals((String) "iperf")) {
                    commandList.remove(0);
                }
                //The execution command is added first in the list for the shell interface.
                commandList.add(0, iperfFile);

                //The process is now being run with the verified parameters.
                process = new ProcessBuilder().command(commandList).redirectErrorStream(true).start();
                //A buffered output of the stdout is being initialized so the iperf output could be displayed on the screen.
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                //The output text is accumulated into a string buffer and published to the GUI
                char[] buffer = new char[4096];
                StringBuffer output = new StringBuffer();
                while ((read = reader.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                    //This is used to pass the output to the thread running the GUI, since this is separate thread.
                    publishProgress(output.toString());
                    Log.d("fuck this", output.toString());
                    output.delete(0, output.length());
                }
                reader.close();
                process.destroy();
            } catch (IOException e) {
                publishProgress("\nError occurred while accessing system resources, please reboot and try again.");
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPreExecute() {
//            Toast.makeText(MainActivity.this, "Starting Iperf", Toast.LENGTH_SHORT).show();
            super.onPreExecute();
        }

        //This function is called by AsyncTask when publishProgress is called.
        //This function runs on the main GUI thread so it can publish changes to it, while not getting in the way of the main task.
        @Override
        public void onProgressUpdate(String... strings) {
//            tv.append(strings[0]);
            //The next command is used to roll the text to the bottom
//            scroller.post(new Runnable() {
//                public void run() {
//                    scroller.smoothScrollTo(0, tv.getBottom());
//                }
//            });
        }

        //This function is called by the AsyncTask class when IperfTask.cancel is called.
        //It is used to terminate an already running task.
        @Override
        public void onCancelled() {
            //The running process is destroyed and system resources are freed.
            if (process != null) {
                process.destroy();
                try {
                    process.waitFor();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            //The toggle button is switched to "off"
//            toggleButton.setChecked(false);
//            tv.append("\nOperation aborted.\n\n");
            //The next command is used to roll the text to the bottom
//            scroller.post(new Runnable() {
//                public void run() {
//                    scroller.smoothScrollTo(0, tv.getBottom());
//                }
//            });
        }

        @Override
        public void onPostExecute(String result) {
            //The running process is destroyed and system resources are freed.
            if (process != null) {
                process.destroy();

                try {
                    process.waitFor();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
//                tv.append("\nTest is done.\n\n");
            }
            //The toggle button is switched to "off"
//            toggleButton.setChecked(false);
//            //The next command is used to roll the text to the bottom
//            scroller.post(new Runnable() {
//                public void run() {
//                    scroller.smoothScrollTo(0, tv.getBottom());
//                }
//            });
        }
    }


}