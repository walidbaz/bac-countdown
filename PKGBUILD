# Maintainer: Bazizi Walid <walidbaz@users.noreply.github.com>
pkgname=bac-countdown
pkgver=1.0
pkgrel=1
pkgdesc="Live BAC exam countdown script"
arch=('any')
url="https://github.com/walidbaz/bac-countdown"
license=('MIT')
depends=('python' 'python-requests' 'python-beautifulsoup4')
source=("https://github.com/walidbaz/bac-countdown/archive/refs/tags/v1.0.tar.gz")
sha256sums=('SKIP') # You can calculate later with sha256sum

package() {
    mkdir -p "$pkgdir/usr/bin"
    install -Dm755 "bac_date.py" "$pkgdir/usr/bin/bac-countdown"
}
