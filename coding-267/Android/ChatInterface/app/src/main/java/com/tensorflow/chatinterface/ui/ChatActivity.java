package com.tensorflow.chatinterface.ui;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.Toolbar;
import android.text.TextUtils;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.tensorflow.chatinterface.R;
import com.tensorflow.chatinterface.util.StringUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ChatActivity extends BaseActivity {
    private static final String TAG = ChatActivity.class.getSimpleName();

    private static final int REQUEST_PERMISSION = 1;
    private final int VIEW_TYPE = 0xb01;
    private final int MESSAGE = 0xb02;
    private final int VIEW_TYPE_LEFT = -10;
    private final int VIEW_TYPE_RIGHT = -11;
    private ListView mListView;
    private MessageAdapter mAdapter;
    private EditText mEtMessageInput;
    private ImageView mBtnSend, mBtnPhonetics;
    private ArrayList<HashMap<Integer, Object>> mItems = null;
    private Toolbar mToolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
        setContentView(R.layout.base_chart);
        super.onCreate(savedInstanceState);

        checkPermissions();
        initToolbar();
        initViews();
    }

    /**
     * 检查Android 6.0之后的运行时权限
     */
    private void checkPermissions() {
        List<String> permissionList = new ArrayList<>();
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.ACCESS_COARSE_LOCATION);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.ACCESS_FINE_LOCATION);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.RECORD_AUDIO);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.READ_PHONE_STATE);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.READ_CONTACTS);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionList.add(Manifest.permission.WRITE_EXTERNAL_STORAGE);
        }
        if (!permissionList.isEmpty()) {
            String[] permissions = permissionList.toArray(new String[permissionList.size()]);
            ActivityCompat.requestPermissions(this, permissions, REQUEST_PERMISSION);
        } else {
            Log.d(TAG, "权限已经获取");
        }
    }

    /**
     * 初始化Toolbar
     */
    private void initToolbar() {
        mToolbar = findViewById(R.id.toolbar);
        setSupportActionBar(mToolbar);
        ((TextView) mToolbar.findViewById(R.id.title_toolbar)).setText("ChatRobot");
    }

    /**
     * 初始化控件参数
     */
    private void initViews() {
        mItems = new ArrayList<>();
        mListView = findViewById(android.R.id.list);
        mAdapter = new MessageAdapter(this, -1);
        mListView.setAdapter(mAdapter);
        mEtMessageInput = findViewById(R.id.edit_send);
        mBtnSend = findViewById(R.id.btn_send);
        mBtnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = mEtMessageInput.getText().toString();
                if(TextUtils.isEmpty(message)){
                    Toast.makeText(ChatActivity.this, "请输入你要说的话", Toast.LENGTH_SHORT).show();
                    return;
                }
                mEtMessageInput.setText(null);
                refreshUi(message, VIEW_TYPE_RIGHT);
            }
        });
        mBtnPhonetics = findViewById(R.id.btn_phonetics);
        mBtnPhonetics.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(ChatActivity.this, "本版本暂不支持语音输入", Toast.LENGTH_SHORT).show();
            }
        });
    }

    /**
     * 刷新消息界面规则
     *
     * @param message
     */
    private void msgToTfLite(String message) {
        String received = "";
        if (message.equals(StringUtils.sSendTo[0])) {
            received = StringUtils.sSendReceived[0];
        } else if (message.equals(StringUtils.sSendTo[1])) {
            received = StringUtils.sSendReceived[1];
        } else if (message.equals(StringUtils.sSendTo[2])) {
            received = StringUtils.sSendReceived[2];
        } else if (message.equals(StringUtils.sSendTo[3])) {
            received = StringUtils.sSendReceived[3];
        } else if (message.equals(StringUtils.sSendTo[4])) {
            received = StringUtils.sSendReceived[4];
        } else if (message.equals(StringUtils.sSendTo[5])) {
            received = StringUtils.sSendReceived[5];
        } else {
            received = message;
        }
        refreshUi(received, VIEW_TYPE_LEFT);
    }

    /**
     * 刷新消息界面具体
     *
     * @param msg
     */
    private void refreshUi(String msg, int msgType) {
        if (TextUtils.isEmpty(msg)) {
            Toast.makeText(this, "无效输入|-。-|try again later", Toast.LENGTH_SHORT).show();
            return;
        }
        HashMap<Integer, Object> map = new HashMap<>();
        map.put(VIEW_TYPE, msgType);
        map.put(MESSAGE, msg);
        mItems.add(map);
        mAdapter.notifyDataSetChanged();
        if (msgType == VIEW_TYPE_RIGHT) {
            msgToTfLite(msg);
        }
    }

    /**
     * ListView的Adapter
     */
    private class MessageAdapter extends ArrayAdapter {
        private LayoutInflater layoutInflater;

        public MessageAdapter(Context context, int resource) {
            super(context, resource);
            layoutInflater = LayoutInflater.from(context);
        }

        @Override
        public View getView(int pos, View convertView, ViewGroup parent) {
            int type = getItemViewType(pos);
            String msg = getItem(pos);
            switch (type) {
                case VIEW_TYPE_LEFT:
                    convertView = layoutInflater.inflate(R.layout.base_left_usr, null);
                    TextView textLeft = convertView.findViewById(R.id.usr_msg);
                    textLeft.setText(msg);
                    break;

                case VIEW_TYPE_RIGHT:
                    convertView = layoutInflater.inflate(R.layout.base_right_usr, null);
                    TextView textRight = convertView.findViewById(R.id.usr_msg);
                    textRight.setText(msg);
                    break;
            }
            return convertView;
        }

        @Override
        public String getItem(int pos) {
            String s = mItems.get(pos).get(MESSAGE) + "";
            return s;
        }

        @Override
        public int getCount() {
            return mItems.size();
        }

        @Override
        public int getItemViewType(int pos) {
            int type = (Integer) mItems.get(pos).get(VIEW_TYPE);
            return type;
        }

        @Override
        public int getViewTypeCount() {
            return 2;
        }

    }
}
