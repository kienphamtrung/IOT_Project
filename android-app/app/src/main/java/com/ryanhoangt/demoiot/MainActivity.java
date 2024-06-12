package com.ryanhoangt.demoiot;

import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private MQTTHelper mqttHelper;
    private TextView txtTemp, txtHumid;
    private EditText inputCycle,
            inputFlow1,
            inputFlow2,
            inputFlow3,
            inputSchedulerName,
            inputStartTime,
            inputStopTime;
    private Button submitButton;
    private LinearLayout jobContainer;
    private List<View> tasksViewList;
    private List<Task> tasksList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
//        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
//            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
//            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
//            return insets;
//        });

        inputCycle = findViewById(R.id.inputCycle);
        inputFlow1 = findViewById(R.id.inputFlow1);
        inputFlow2 = findViewById(R.id.inputFlow2);
        inputFlow3 = findViewById(R.id.inputFlow3);
        inputSchedulerName = findViewById(R.id.inputSchedulerName);
        inputStartTime = findViewById(R.id.inputStartTime);
        inputStopTime = findViewById(R.id.inputStopTime);
        submitButton = findViewById(R.id.submitButton);
        txtTemp = findViewById(R.id.txtTemp);
        txtHumid = findViewById(R.id.txtHumid);
        jobContainer = findViewById(R.id.jobContainer);
        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                handleSubmit();
            }
        });
        tasksViewList = new ArrayList<>();
        tasksList = new ArrayList<>();

        startMQTT();
    }

    private void handleSubmit() {
        int cycle = Integer.parseInt(inputCycle.getText().toString());
        int flow1 = Integer.parseInt(inputFlow1.getText().toString());
        int flow2 = Integer.parseInt(inputFlow2.getText().toString());
        int flow3 = Integer.parseInt(inputFlow3.getText().toString());
//        boolean isActive = true;
        String schedulerName = inputSchedulerName.getText().toString();
        String startTime = inputStartTime.getText().toString();
        String stopTime = inputStopTime.getText().toString();

        JSONObject dataObj = new JSONObject();
        try {
            dataObj.put("cycle", cycle);
            dataObj.put("flow1", flow1);
            dataObj.put("flow2", flow2);
            dataObj.put("flow3", flow3);
            dataObj.put("isActive", true);
            dataObj.put("schedulerName", schedulerName);
            dataObj.put("startTime", startTime);
            dataObj.put("stopTime", stopTime);
        } catch (JSONException e) {
            Toast toast = Toast.makeText(this, "Error creating JSON: " + e.getMessage(), Toast.LENGTH_SHORT);
            toast.setGravity(Gravity.TOP|Gravity.CENTER_HORIZONTAL, 0, 0);
            toast.show();
        }

        // Handle the input data as needed
        sendDataMQTT("ryanhoangt/feeds/irrigation-tasks", dataObj.toString());
        sendDataMQTT("ryanhoangt/feeds/sched" + (tasksList.size() + 1), dataObj.toString());
        Toast toast = Toast.makeText(this, "Data submitted!", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP|Gravity.CENTER_HORIZONTAL, 0, 0);
        toast.show();

        // Construct a Task object
        Task task = new Task(
                schedulerName,
                cycle,
                flow1,
                flow2,
                flow3,
                startTime,
                stopTime
        );

        if (!schedulerName.isEmpty()) {
            addJob(task);
            inputSchedulerName.setText(""); // Clear the input field
        }
    }

    private void addJob(Task task) {
        // Inflate the job item layout
        View jobItem = LayoutInflater.from(this).inflate(R.layout.job_item, jobContainer, false);

        // Find the TextView and ToggleButton in the job item layout
        TextView jobName = jobItem.findViewById(R.id.jobName);
        TextView jobIdView = jobItem.findViewById(R.id.jobId);
        ToggleButton jobToggleButton = jobItem.findViewById(R.id.jobToggleButton);

        // Set the job name
        jobName.setText(task.getSchedulerName());
        jobIdView.setText("" + tasksList.size());
        jobToggleButton.setChecked(true);

        jobToggleButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("BTN MESSAGE: ", "!!!toggle btn clicked!!!!!!");
                int jobId = Integer.parseInt(jobIdView.getText().toString());
                Task curTask = tasksList.get(jobId);
                Log.d("TEST MESSAGE: ", "---" + curTask.toString());

                JSONObject dataObj = new JSONObject();
                try {
                    dataObj.put("cycle", curTask.getCycle());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getCycle());
                    dataObj.put("flow1", curTask.getFlow1());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getFlow1());
                    dataObj.put("flow2", curTask.getFlow2());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getFlow2());
                    dataObj.put("flow3", curTask.getFlow3());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getFlow3());
                    dataObj.put("isActive", !curTask.isActive());
                    Log.d("TEST MESSAGE: ", "---" + curTask.isActive());
                    dataObj.put("schedulerName", curTask.getSchedulerName());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getSchedulerName());
                    dataObj.put("startTime", curTask.getStartTime());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getStartTime());
                    dataObj.put("stopTime", curTask.getStopTime());
                    Log.d("TEST MESSAGE: ", "---" + curTask.getStopTime());
                } catch (JSONException e) {
                }
                curTask.setActive(!curTask.isActive());
                // Handle the input data as needed
                sendDataMQTT("ryanhoangt/feeds/sched" + (jobId + 1), dataObj.toString());
            }
        });

        // Add the job item to the container
        jobContainer.addView(jobItem);
        tasksViewList.add(jobItem);
        tasksList.add(task);
    }

    private void sendDataMQTT(String topic, String value) {
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }

    private void startMQTT() {
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST MESSAGE: ", topic + "---" + message.toString());

                if (topic.contains("cambien1")) {
                    txtTemp.setText(message.toString() + "*C");
                } else if (topic.contains("cambien2")) {
                    txtHumid.setText(message.toString() + "%");
                } else if (topic.contains("stage")) {
                    String msg = message.toString();

                    String[] numbers = msg.split(",");
                    int taskId = Integer.parseInt(numbers[0].trim());
                    int cycle = Integer.parseInt(numbers[1].trim());
                    int status = Integer.parseInt(numbers[2].trim());

                    View taskView = tasksViewList.get(taskId);

                    // Set cycle
                    TextView cycleView = taskView.findViewById(R.id.jobCycle);
                    tasksList.get(taskId).setCurCycle(cycle);
                    cycleView.setText("Cycle " + cycle);

                    // Set status
                    TextView jobStatusView = taskView.findViewById(R.id.jobStatus);
                    tasksList.get(taskId).setStatus(status);
                    jobStatusView.setText(tasksList.get(taskId).getStatus());
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}


//public class MainActivity extends AppCompatActivity {
//
//    private MQTTHelper mqttHelper;
//    private TextView txtTemp, txtHumid;
//    private LabeledSwitch btnLED, btnPUMP;
//
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        EdgeToEdge.enable(this);
//        setContentView(R.layout.activity_main);
//        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
//            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
//            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
//            return insets;
//        });
//
//        txtTemp = findViewById(R.id.txtTemp);
//        txtHumid = findViewById(R.id.txtHumid);
//        btnLED = findViewById(R.id.btnLED);
//        btnPUMP = findViewById(R.id.btnPUMP);
//
//        btnLED.setOnToggledListener(new OnToggledListener() {
//            @Override
//            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
//                if (isOn) {
//                    sendDataMQTT("ryanhoangt/feeds/nutnhan1", "1");
//                } else {
//                    sendDataMQTT("ryanhoangt/feeds/nutnhan1", "0");
//                }
//            }
//        });
//        btnPUMP.setOnToggledListener(new OnToggledListener() {
//            @Override
//            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
//                if (isOn) {
//                    sendDataMQTT("ryanhoangt/feeds/nutnhan2", "1");
//                } else {
//                    sendDataMQTT("ryanhoangt/feeds/nutnhan2", "0");
//                }
//            }
//        });
//
//        startMQTT();
//    }
//
//    private void sendDataMQTT(String topic, String value) {
//        MqttMessage msg = new MqttMessage();
//        msg.setId(1234);
//        msg.setQos(0);
//        msg.setRetained(false);
//
//        byte[] b = value.getBytes(Charset.forName("UTF-8"));
//        msg.setPayload(b);
//
//        try {
//            mqttHelper.mqttAndroidClient.publish(topic, msg);
//        }catch (MqttException e){
//        }
//    }
//
//    private void startMQTT() {
//        mqttHelper = new MQTTHelper(this);
//        mqttHelper.setCallback(new MqttCallbackExtended() {
//            @Override
//            public void connectComplete(boolean reconnect, String serverURI) {
//
//            }
//
//            @Override
//            public void connectionLost(Throwable cause) {
//
//            }
//
//            @Override
//            public void messageArrived(String topic, MqttMessage message) throws Exception {
//                Log.d("TEST MESSAGE: ", topic + "---" + message.toString());
//
//                if (topic.contains("cambien1")) {
//                    txtTemp.setText(message.toString() + "*C");
//                } else if (topic.contains("cambien2")) {
//                    txtHumid.setText(message.toString() + "%");
//                } else if (topic.contains("nutnhan1")) {
//                    if (message.toString().equals("1")) {
//                        btnLED.setOn(true);
//                    } else {
//                        btnLED.setOn(false);
//                    }
//                } else if (topic.contains("nutnhan2")) {
//                    if (message.toString().equals("1")) {
//                        btnPUMP.setOn(true);
//                    } else {
//                        btnPUMP.setOn(false);
//                    }
//                }
//            }
//
//            @Override
//            public void deliveryComplete(IMqttDeliveryToken token) {
//
//            }
//        });
//    }
//}