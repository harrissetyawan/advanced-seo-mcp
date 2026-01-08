# Blog Yazısı: AI Ajanları için Gelişmiş SEO Araçları Nasıl Kurulur?

Yapay zeka asistanları (LLM'ler) hayatımızın merkezine yerleşti. Ancak bir web geliştiricisi veya SEO uzmanı olarak, AI'nın en büyük eksikliğini fark etmişsinizdir: **Gerçek zamanlı ve güvenilir SEO verisine erişim.**

Claude veya ChatGPT'ye "Sitemin SEO durumu nasıl?" diye sorduğunuzda, genellikle genel-geçer cevaplar alırsınız veya "Ben internete erişemiyorum" yanıtıyla karşılaşırsınız.

İşte **Advanced SEO MCP Server** tam bu noktada devreye giriyor.

## 🛠️ Model Context Protocol (MCP) Nedir?

MCP, AI modellerinin dış dünyadaki araçları (veritabanları, API'ler, terminal) güvenli bir şekilde kullanmasını sağlayan yeni bir standarttır. Ben de bu standardı kullanarak, AI ajanlarına profesyonel bir SEO uzmanının yeteneklerini kazandıran bir sunucu geliştirdim.

## 📦 Projenin Özellikleri

Bu proje, basit bir HTML ayrıştırıcısının çok ötesinde. İçerisinde şunları barındırıyor:

1.  **Ahrefs Entegrasyonu:** CapSolver API kullanarak Ahrefs'in güvenlik duvarlarını (yasal sınırlar içinde) aşıyor ve sitenizin Backlink/DR verilerini çekiyor.
2.  **Google PageSpeed Insights:** API üzerinden sitenizin mobil ve masaüstü hız skorlarını (LCP, CLS) anlık ölçüyor.
3.  **Teknik Denetim:**
    *   **Schema Validator:** JSON-LD yapınızın Google standartlarına uygun olup olmadığını kontrol ediyor.
    *   **Broken Link Checker:** Sayfadaki tüm dış linkleri tarayıp 404 verenleri raporluyor.
    *   **Keyword Density:** İçerik analizi yaparak anahtar kelime yoğunluğunu hesaplıyor.

## 🚀 Nasıl Kullanılır?

Kurulum oldukça basit. Python tabanlı olduğu için `pip` ile kurabilirsiniz:

```bash
pip install advanced-seo-mcp
```

Ardından, Cursor veya Claude Desktop yapılandırmanıza eklemeniz yeterli. Proje, kurulumu otomatize eden bir `setup_extension.py` betiği ile geliyor.

## 📊 Örnek Senaryo

Cursor editöründesiniz ve yeni bir blog sayfası tasarlıyorsunuz. AI asistanına şunu diyebilirsiniz:

> "Şu anki sayfamı rakibim olan 'example.com' ile kıyasla ve eksik olduğum Schema yapılarını listele."

Advanced SEO MCP, arka planda her iki siteyi tarayacak, Ahrefs verilerini çekecek, Schema yapılarını karşılaştıracak ve size maddeler halinde bir yapılacaklar listesi sunacaktır.

## 🔗 İndirin ve Deneyin

Proje tamamen açık kaynak. GitHub üzerinden inceleyebilir, katkıda bulunabilir veya kendi ihtiyaçlarınıza göre çatallayabilirsiniz.

**GitHub:** [https://github.com/halilertekin/advanced-seo-mcp](https://github.com/halilertekin/advanced-seo-mcp)
**PyPI:** [https://pypi.org/project/advanced-seo-mcp/](https://pypi.org/project/advanced-seo-mcp/)
