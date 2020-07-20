package com.gco.pidcee2

import android.bluetooth.BluetoothDevice
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView

data class BluetoothRecord(val bluetoothDevice: BluetoothDevice, var lastKnownRssi: Int = -1)

class BluetoothDeviceAdapter(private val context: Context) : BaseAdapter() {

    // Map by address of bluetooth devices
    private val deviceRecords = ArrayList<BluetoothRecord>()

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val adapterView =
            convertView ?: LayoutInflater.from(context)
                .inflate(android.R.layout.simple_list_item_1, parent, false)
        val item = getItem(position)
        adapterView.findViewById<TextView>(android.R.id.text1).text =
            "${item.bluetoothDevice.name}: ${item.lastKnownRssi}\n${item.bluetoothDevice.address}"
        return adapterView
    }

    override fun getItem(position: Int): BluetoothRecord = deviceRecords[position]
    override fun getItemId(position: Int) = 0L

    override fun getCount() = deviceRecords.size

    fun addDevice(bluetoothDevice: BluetoothDevice, rssi: Int = -1) {
        deviceRecords.removeAll { it.bluetoothDevice.address == bluetoothDevice.address }
        deviceRecords.add(BluetoothRecord(bluetoothDevice, rssi))
        deviceRecords.sortBy { it.lastKnownRssi }
        notifyDataSetInvalidated()
    }

    fun removeDevice(bluetoothDevice: BluetoothDevice) {
        if (deviceRecords.removeAll { it.bluetoothDevice.address == bluetoothDevice.address })
            notifyDataSetInvalidated()
    }

    fun clearDevices() {
        deviceRecords.clear()
        notifyDataSetInvalidated()
    }
}
