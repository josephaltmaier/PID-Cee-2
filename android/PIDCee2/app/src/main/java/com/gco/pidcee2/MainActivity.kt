package com.gco.pidcee2

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ListView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private val receiver: BroadcastReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            when (intent.action) {
                BluetoothDevice.ACTION_FOUND -> bluetoothAdapter.addDevice(
                    intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)!!,
                    intent.getIntExtra(BluetoothDevice.EXTRA_RSSI, -1)
                )
            }
        }
    }
    private lateinit var displayText: TextView
    private lateinit var deviceList: ListView
    private lateinit var bluetoothAdapter: BluetoothDeviceAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        when (ContextCompat.checkSelfPermission(this, "android.permission.BLUETOOTH"))
        {
            PackageManager.PERMISSION_GRANTED -> setupButtons()
            PackageManager.PERMISSION_DENIED -> Log.e("MYTAG", "Whoops no permission")
        }
    }

    private fun setupButtons() {
        val stopScanButton = findViewById<Button>(R.id.stop_scan_button)
        val startScanButtonScanButton = findViewById<Button>(R.id.start_scan_button)
        val readRssiButton = findViewById<Button>(R.id.read_rssi)

        displayText = findViewById(R.id.display_text)
        deviceList = findViewById(R.id.device_list)
        bluetoothAdapter = BluetoothDeviceAdapter(this)
        deviceList.adapter = bluetoothAdapter
        deviceList.setOnItemClickListener {
                _, _, position, _ ->
            startActivity(BluetoothDeviceDisplayActivityIntent(bluetoothAdapter.getItem(position)))
        }


        stopScanButton.setOnClickListener {
            it.isEnabled = false
            readRssiButton.isEnabled = false
            startScanButtonScanButton.isEnabled = true
            unregisterReceiver(receiver)
            BluetoothAdapter.getDefaultAdapter().cancelDiscovery()
            bluetoothAdapter.clearDevices()
        }

        startScanButtonScanButton.setOnClickListener {
            it.isEnabled = false
            stopScanButton.isEnabled = true
            readRssiButton.isEnabled = true
            displayText.text = "Starting Scan"
            BluetoothAdapter.getDefaultAdapter().startDiscovery()
            registerReceiver(receiver, IntentFilter(BluetoothDevice.ACTION_FOUND))
            BluetoothAdapter.getDefaultAdapter().bondedDevices.forEach { device ->
                bluetoothAdapter.addDevice(device)
            }
        }

        readRssiButton.setOnClickListener {
            BluetoothAdapter.getDefaultAdapter().bondedDevices.forEach { device ->
                bluetoothAdapter.addDevice(device)
                device.connectGatt(this, true,
                    object : BluetoothGattCallback() {
                        override fun onConnectionStateChange(
                            gatt: BluetoothGatt?,
                            status: Int,
                            newState: Int
                        ) {
                            super.onConnectionStateChange(gatt, status, newState)
                            bluetoothAdapter.addDevice(device, -2)
                            gatt?.readRemoteRssi()
                        }

                        override fun onReadRemoteRssi(
                            gatt: BluetoothGatt?,
                            rssi: Int,
                            status: Int
                        ) {
                            super.onReadRemoteRssi(gatt, rssi, status)
                            if (status == BluetoothGatt.GATT_SUCCESS) {
                                bluetoothAdapter.addDevice(device, rssi)
                            }
                        }
                    }
                )
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(receiver)
    }
}

