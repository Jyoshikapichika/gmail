package com.college.gmaildemo;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import androidx.core.content.FileProvider;
import com.getcapacitor.BridgeActivity;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getBridge() != null && getBridge().getWebView() != null) {
            WebView webView = getBridge().getWebView();
            webView.addJavascriptInterface(new AndroidPdfBridge(), "AndroidPdfBridge");
        }
    }

    public class AndroidPdfBridge {
        @JavascriptInterface
        public String downloadAndOpenPdf(String fileName) {
            String safeName = (fileName != null && !fileName.isEmpty())
                ? fileName
                : "NOC26CS93S370700875.pdf";
            try {
                // 1. Copy unmodified PDF from bundled APK assets into cache dir for FileProvider viewing
                File outCacheFile = new File(getCacheDir(), safeName);
                try (InputStream in = getAssets().open("public/" + safeName);
                     FileOutputStream out = new FileOutputStream(outCacheFile)) {
                    byte[] buffer = new byte[65536];
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        out.write(buffer, 0, read);
                    }
                    out.flush();
                }

                // 2. Also save to the device's public Downloads folder (Android 10+ MediaStore)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    try {
                        ContentResolver resolver = getContentResolver();
                        ContentValues values = new ContentValues();
                        values.put(MediaStore.Downloads.DISPLAY_NAME, safeName);
                        values.put(MediaStore.Downloads.MIME_TYPE, "application/pdf");
                        values.put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS);
                        Uri downloadUri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
                        if (downloadUri != null) {
                            try (InputStream in2 = getAssets().open("public/" + safeName);
                                 OutputStream out2 = resolver.openOutputStream(downloadUri)) {
                                if (out2 != null) {
                                    byte[] buf = new byte[65536];
                                    int r;
                                    while ((r = in2.read(buf)) != -1) {
                                        out2.write(buf, 0, r);
                                    }
                                    out2.flush();
                                }
                            }
                        }
                    } catch (Exception ignored) {
                        // Continue to open PDF via FileProvider even if Downloads write already exists
                    }
                }

                // 3. Launch native Android PDF viewer via FileProvider
                Uri contentUri = FileProvider.getUriForFile(
                    MainActivity.this,
                    getPackageName() + ".fileprovider",
                    outCacheFile
                );
                Intent viewIntent = new Intent(Intent.ACTION_VIEW);
                viewIntent.setDataAndType(contentUri, "application/pdf");
                viewIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
                runOnUiThread(() -> {
                    try {
                        startActivity(Intent.createChooser(viewIntent, "Open Hall Ticket PDF"));
                    } catch (Exception ignored) {}
                });

                return "Saved " + safeName + " to Downloads and opening PDF...";
            } catch (Exception e) {
                return "Error opening PDF: " + e.getMessage();
            }
        }
    }
}
