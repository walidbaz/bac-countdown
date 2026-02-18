# Maintainer: Bazizi Walid
pkgname=bac-countdown
pkgver=1.0.0
pkgrel=1
pkgdesc="Terminal live countdown to the BAC exam"
arch=('x86_64')
url="https://eddirasa.com/العد-التنازلي-لموعد-البكالوريا/"
license=('MIT')
depends=('python' 'python-requests' 'python-beautifulsoup4')
source=("bac_date.py")
sha256sums=('SKIP')

package() {
    install -Dm755 "$srcdir/bac_date.py" "$pkgdir/usr/bin/bac-countdown"
}
