# Attendance System - Quick Setup Script for XAMPP
# This script copies files to XAMPP htdocs directory

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Attendance System - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if XAMPP is installed
$xamppPath = "C:\xampp"
if (-not (Test-Path $xamppPath)) {
    Write-Host "❌ XAMPP not found at $xamppPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install XAMPP from: https://www.apachefriends.org/" -ForegroundColor Yellow
    Write-Host "Or update the `$xamppPath variable in this script if installed elsewhere" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✅ XAMPP found at $xamppPath" -ForegroundColor Green

# Source directory (current location)
$sourceDir = "e:\git\Attendance management System"

# Destination directory
$destDir = "$xamppPath\htdocs\attendance"

# Create destination directory
Write-Host ""
Write-Host "Creating directory: $destDir" -ForegroundColor Yellow
try {
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Write-Host "✅ Directory created" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creating directory: $_" -ForegroundColor Red
    pause
    exit
}

# Files to copy (PHP/HTML system)
$files = @(
    "attendance.html",
    "attendance_form.php",
    "db_connect.php",
    "database_setup.sql",
    "test_db.php",
    "README.md",
    "HTML_TESTING_GUIDE.md"
)

Write-Host ""
Write-Host "Copying files..." -ForegroundColor Yellow

$successCount = 0
$failCount = 0

foreach ($file in $files) {
    $sourcePath = Join-Path $sourceDir $file
    $destPath = Join-Path $destDir $file
    
    if (Test-Path $sourcePath) {
        try {
            Copy-Item $sourcePath $destPath -Force
            Write-Host "  ✓ $file" -ForegroundColor Green
            $successCount++
        } catch {
            Write-Host "  ✗ $file - Error: $_" -ForegroundColor Red
            $failCount++
        }
    } else {
        Write-Host "  ✗ $file - Not found in source" -ForegroundColor Red
        $failCount++
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files copied: $successCount" -ForegroundColor Green
Write-Host "Files failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($successCount -gt 0) {
    Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Start XAMPP Control Panel" -ForegroundColor White
    Write-Host "2. Start Apache and MySQL services" -ForegroundColor White
    Write-Host "3. Import database:" -ForegroundColor White
    Write-Host "   - Open: http://localhost/phpmyadmin" -ForegroundColor Cyan
    Write-Host "   - Go to SQL tab" -ForegroundColor Cyan
    Write-Host "   - Import: $destDir\database_setup.sql" -ForegroundColor Cyan
    Write-Host "4. Test database connection:" -ForegroundColor White
    Write-Host "   - Open: http://localhost/attendance/test_db.php" -ForegroundColor Cyan
    Write-Host "5. Run the application:" -ForegroundColor White
    Write-Host "   - Open: http://localhost/attendance/attendance.html" -ForegroundColor Cyan
    Write-Host ""
    
    # Ask if user wants to open URLs
    $openBrowser = Read-Host "Open browser to test database? (y/n)"
    if ($openBrowser -eq 'y' -or $openBrowser -eq 'Y') {
        Start-Process "http://localhost/attendance/test_db.php"
    }
} else {
    Write-Host "❌ Setup failed. Please check errors above." -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
