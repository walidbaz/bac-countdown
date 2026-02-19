# Maintainer: Bazizi Walid <walidbaz@users.noreply.github.com>

pkgname=bac-countdown
pkgver=1.1
pkgrel=1
pkgdesc="Live BAC exam countdown script"
arch=('any')
url="https://github.com/walidbaz/bac-countdown"
license=('MIT')
depends=('python' 'python-requests' 'python-beautifulsoup4' 'python-rich')
source=("$pkgname-$pkgver.tar.gz::https://github.com/walidbaz/bac-countdown/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # You can calculate later with sha256sum
package() {
    # Automatically detect the extracted folder
    extracted_folder=$(find "$srcdir" -mindepth 1 -maxdepth 1 -type d)
    cd "$extracted_folder"

    install -Dm755 bac_date.py "$pkgdir/usr/bin/bac-countdown"
}
