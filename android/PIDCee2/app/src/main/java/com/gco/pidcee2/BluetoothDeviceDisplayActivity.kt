package com.gco.pidcee2

import android.bluetooth.BluetoothDevice
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

fun Context.BluetoothDeviceDisplayActivityIntent(bluetoothRecord: BluetoothRecord): Intent {
    return Intent(this, BluetoothDeviceDisplayActivity::class.java).apply {
        putExtra(BluetoothDevice.EXTRA_DEVICE, bluetoothRecord.bluetoothDevice)
    }
}

class BluetoothDeviceDisplayActivity : AppCompatActivity() {

    private lateinit var bluetoothDevice: BluetoothDevice

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_bluetooth_display)
        setSupportActionBar(findViewById(R.id.toolbar))

        bluetoothDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)!!
        title = bluetoothDevice.name ?: bluetoothDevice.address

        findViewById<TextView>(R.id.device_overview).text =
            """
            Name: ${bluetoothDevice.name}
            Address: ${bluetoothDevice.address}
            Type: ${bluetoothDevice.type.toBluetoothDeviceType()}
            BondState: ${bluetoothDevice.bondState.toBondState()}
            UUID: ${bluetoothDevice.uuids}
            """.trimIndent()
    }
}

private fun Int.toBondState() = when(this) {
    BluetoothDevice.BOND_NONE -> "NONE"
    BluetoothDevice.BOND_BONDED -> "BONDED"
    BluetoothDevice .BOND_BONDING -> "BONDING"
    else -> "UNKNOWN"
}

private fun Int.toBluetoothDeviceType() = when(this) {
    BluetoothDevice.DEVICE_TYPE_CLASSIC -> "CLASSIC"
    BluetoothDevice.DEVICE_TYPE_DUAL -> "DUAL"
    BluetoothDevice.DEVICE_TYPE_LE -> "LE"
    else -> "UNKNOWN"
}