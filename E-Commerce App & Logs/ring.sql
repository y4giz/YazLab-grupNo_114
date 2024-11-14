-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 06 Şub 2023, 11:12:18
-- Sunucu sürümü: 10.4.24-MariaDB
-- PHP Sürümü: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `ring`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `addresses`
--

CREATE TABLE `addresses` (
  `address_id` int(11) NOT NULL,
  `user_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `address_header` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(500) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `addresses`
--

INSERT INTO `addresses` (`address_id`, `user_id`, `address_header`, `address`) VALUES
(1, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', 'test address headerssdssd', 'test address content'),
(2, 'b6f0c4d8-2f77-437f-bcd0-e0d6be95d4b6', 'HOME', '8613 Saxon Road\nKennesaw, GA 30144');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `baskets`
--

CREATE TABLE `baskets` (
  `basket_id` bigint(20) NOT NULL,
  `user_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `orders` varchar(5000) COLLATE utf8_unicode_ci NOT NULL,
  `basket_status` tinyint(4) NOT NULL,
  `basket_total` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `basket_date` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `baskets`
--

INSERT INTO `baskets` (`basket_id`, `user_id`, `orders`, `basket_status`, `basket_total`, `basket_date`) VALUES
(100000, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'3dc6355f-857c-4f10-85fa-97656768c254\', \'1\', 245.0]]', 1, '245.0', '25-01-2023 15:20'),
(100002, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'08389046-a7f3-4230-b27a-e7516b4b1f9d\', \'1\', 80.0]]', 1, '80.0', '25-01-2023 15:31'),
(100003, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'08389046-a7f3-4230-b27a-e7516b4b1f9d\', \'1\', 80.0]]', 1, '80.0', '25-01-2023 15:33'),
(100004, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'12ee6158-b2fd-407c-843b-c54e599e0b9c\', \'2\', 300.0], [\'08389046-a7f3-4230-b27a-e7516b4b1f9d\', \'1\', 80.0]]', 1, '380.0', '25-01-2023 15:57'),
(100005, 'b6f0c4d8-2f77-437f-bcd0-e0d6be95d4b6', '[[\'08389046-a7f3-4230-b27a-e7516b4b1f9d\', \'2\', 160.0]]', 1, '160.0', '25-01-2023 22:01'),
(100007, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'024b8617-7e49-4b70-afd5-2b844b47aa9\', \'1\', 850.0]]', 1, '850.0', '04-02-2023 19:39'),
(100010, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '[[\'47160883-982c-11ed-a2a5-e2e61a8eed50\', \'1\', 1000.0], [\'024b8617-7e49-4b70-afd5-2b844b47aa9\', \'-1\', -850.0]]', 1, '1.0', '06-02-2023 12:02');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`) VALUES
(1, 'Golden Rings'),
(2, 'Solitaire Rings'),
(3, 'Diamond Rings'),
(4, 'Emerald Rings');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `comment_rating` tinyint(4) NOT NULL,
  `comment_review` varchar(300) COLLATE utf8_unicode_ci NOT NULL,
  `comment_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `comment_email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `product_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contacts`
--

CREATE TABLE `contacts` (
  `contact_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `contact_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `contact_email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `contact_subject` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `contact_message` varchar(400) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `contacts`
--

INSERT INTO `contacts` (`contact_id`, `contact_name`, `contact_email`, `contact_subject`, `contact_message`) VALUES
('03474b90-6ddd-472c-bd9b-639c0d006b3a', 'test', 'test@test.com', 'tewrtewt', 'ewtwetwet'),
('37e5fdef-cd92-41b5-9bdc-bd3ed85ec2cd', 'ewfefewf', 'test@test.com', 'fwefewfewf', 'ewfewfewf'),
('45dfc7cb-a187-45b7-a13a-037f80cd2c98', 'test', 'wwfewfewf@cewcwc.com', 'ewfewfew', 'fewfewfewfewf'),
('4ba6f77e-22e5-4e43-bf9a-ac702a6d10a8', '', '', '', ''),
('77e79bfd-9a4a-4ec5-b256-3b1f039a1286', '', '', '', ''),
('84bc05b5-9a9a-42cb-b96e-dd7ac6a46b67', '', '', '', ''),
('a89383fd-3f74-48f6-9e79-f6bc98f6b062', '', '', '', ''),
('af81d06a-f8d4-424e-9154-fee9d6f53082', 'test', 'test@test.local.com', 'tetetet', 'test'),
('b430d5dc-9af0-44fc-85db-538e257f4586', 'rwarrewr', 'test@test.com', 'rwar', 'wrwrwrwr'),
('b524d1cf-6a4e-46cc-ba17-018ae9385323', '', '', '', ''),
('b619a93f-1372-4b61-8b9d-ce967079e0a5', 'fewfewf', 'wwfewfewf@cewcwc.com', 'ewfewfew', 'fewfewfewfewf'),
('f739d97b-727f-473f-90b3-fa466bece077', '', '', '', ''),
('fcf07d8b-6f47-4c13-9417-f3fa8d52981a', '', '', '', '');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `credit_cards`
--

CREATE TABLE `credit_cards` (
  `card_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `card_number` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `card_expiredate` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `card_cvc` int(11) NOT NULL,
  `user_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `products`
--

CREATE TABLE `products` (
  `product_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `product_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `product_price` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `product_image` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `product_description` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
  `category_id` int(11) NOT NULL,
  `product_istrandy` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `product_price`, `product_image`, `product_description`, `category_id`, `product_istrandy`) VALUES
('00902a2e-d7fb-416f-8c71-3b47de26af72', '1.90 carat Cushion Natural Green Emerald Pavé Knife Edge Lotus Basket Engagement Ring', '1500', 'emerald_2_engagement.jpeg', 'You can shop with confidence knowing that every order comes with a James Allen guarantee.', 4, 0),
('024b8617-7e49-4b70-afd5-2b844b47aa9', 'Golden Plated', '850', 'golden_2_goldenplated.jpg', ' This 18k yellow gold plated sterling ring features an art deco inspired starburst pendant ', 1, 0),
('08389046-a7f3-4230-b27a-e7516b4b1f9d', 'Solitaire 925 Silver', '80', 'solitaire_2_925silver.jpg', 'Oval engagement ring 3ct 2ct 1.25ct stone ring Silver ring Promise ring Diamond ring Simulant ring Solitaire ring Gift for her', 2, 0),
('0d9a3176-3347-4c47-9ff8-f7b57617f55d', 'Meenaz Gold', '1100', 'golden_4_meenazgold.jpg', 'Valentine gift Jewellery Stylish Heart Shape Golden Proposal i love you Name Alphabet Letter Initial S Rings for girls women girlfriend Men Boys Couples American diamond CZ AD Adjustable Gifts Set Lovers Design With Velvet Red Rose box set-RING ROSE BOX SET-ME118 Brass, Copper, Crystal, Stone, Alloy, Metal Cubic Zirconia, Diamond, Zircon, Crystal Gold Plated Ring Set', 1, 1),
('12ee6158-b2fd-407c-843b-c54e599e0b9c', '1.0 carat Diamond', '150', 'diamond_2_1.0carat.jpg', 'You\'ll have a naturally timeless elegance when wearing this classic four prong set solitaire ring. An engagement ring that will make the natural shine and brilliance of the diamond stand out on your hand.', 3, 0),
('18faf002-48cc-44f1-862a-caa315f35cc5', 'The One Round Brilliant Diamond Engagement Ring', '1300', 'diamond_1_engagement.jpeg', 'The One, a delicate engagement ring and enduring piece of fine jewelry, features a round brilliant diamond center stone, framed by micropavé diamonds, set on a micropavé band. The timeless glamour of the micropavé setting has quickly become an iconic Harry Winston style. Set in a delicate, feminine design, each diamond engagement ring is meticulously hand-crafted, to highlight the diamond’s graceful beauty.', 3, 0),
('3dc6355f-857c-4f10-85fa-97656768c254', 'Amarino Solitiare', '245', 'solitaire_1_amarino.jpg', 'A beautiful Double halo covered with diamonds for a classic, elegant look.\r\nSolitaire ring mount, with 1.05 carat diamonds certified by IGI. ', 2, 0),
('47160883-982c-11ed-a2a5-e2e61a8eed50', 'Yellow Chims', '1000', 'golden_1_yellow_chims.jpg', 'Product is made with International accepted standard Quality. Nickel and Lead Free products are skin friendly suitable for all age groups.', 1, 1),
('69d6901d-9f74-4cf2-ae31-c7b1d16539de', '1.40 carat Round Natural Green Emerald Solo Infinity Engagement Ring', '2500', 'emerald_1_leviannatural.jpeg', 'Designed to last a lifetime, each piece is beautifully\r\nhandcrafted allowing you to cherish every day while looking gorgeous.', 4, 0),
('6a4f5ca8-e887-4b7b-a50d-d81da2cbe3bf', 'White Gold Round Diamond Engagement Ring', '1300', 'diamond_4_serenaderound.jpg', 'Our boxes are specially designed to complement and protect the jewellery they house. The beautiful faux suede lining combined with the delicate gold details creates a luxurious packaging that will display the jewellery in the best possible way.', 3, 0),
('94c60771-3a4f-4cec-9e32-ad989aec75e1', 'Twisted Halo Diamond Engagement Ring', '1890', 'diamond_3_twistedhalo.jpeg', 'Twisted Halo Diamond Engagement Ring\r\nin 14k White Gold (1/3 ct. tw.)', 3, 0),
('e459130e-a524-4ae5-b939-07ec0b1eb1c3', 'Solitiare Engagement', '850', 'solitaire_3_engagement.jpg', 'This elegant solitaire ring features an open basket with claw prongs that cradle the center gem. The petite band adds to the sleek, classic look of the design. ', 2, 1),
('eb742a2d-a0ab-4103-a6f3-b6b91254271a', '14 Carat Golden', '600', 'golden_3_14karat.jpeg', 'All our diamond suppliers confirm that they comply with the Kimberley Process to ensure that their diamonds are conflict free.', 1, 0),
('f07d808d-2d8c-4ff3-b445-a794242dca45', '0.4 Carat Solitiare', '1400', 'solitaire_4_04carat.jpg', 'engagement ring by Steinberg in White gold (585/1000) with 0,4 ct. brilliant tw,si ', 2, 0);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `reset_tokens`
--

CREATE TABLE `reset_tokens` (
  `token` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` varchar(80) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `reset_tokens`
--

INSERT INTO `reset_tokens` (`token`, `username`, `timestamp`) VALUES
('04891d32-878d-43aa-a1cd-8bc03666574b', 'johndoe', '2023-02-04 16:20:53.442533'),
('4cd29d5c-ab12-40f9-a72b-9b0cb4e82c72', 'test', '2023-02-04 20:24:19.995567'),
('70ba5989-75c2-4172-a045-3da5e1a17092', 'test', '2023-02-04 16:16:20.291938'),
('9f52a7f5-ad7f-460c-9109-82b76c9fec5b', 'test', '2023-02-04 16:20:53.442533'),
('c4228e52-975f-4b65-bf28-01947726edc6', 'test', '2023-02-04 16:17:33.805918'),
('ff2788db-013a-4e7f-9e46-19be6f1af28c', 'test', '2023-02-04 20:21:18.431401');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `subscribers`
--

CREATE TABLE `subscribers` (
  `subscriber_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `subscriber_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `subscriber_email` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `subscribers`
--

INSERT INTO `subscribers` (`subscriber_id`, `subscriber_name`, `subscriber_email`) VALUES
('200a9473-6178-4049-8975-ddf6c428c842', 'tesewt', 'test5@test.com'),
('3c5fa018-8a7d-4701-b5ce-47152a8eef8f', '', 'test@test.com'),
('741f0190-8779-40e6-828f-a881f94a3f2e', 'tsttest testtest', 'test3@test.com'),
('cb3e8a7d-ce38-447b-af37-69456ba64233', '', 'test2@test.com');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `user_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `user_firstname` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `user_lastname` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `user_username` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `user_email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `user_password_hash` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `user_role` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`user_id`, `user_firstname`, `user_lastname`, `user_username`, `user_email`, `user_password_hash`, `user_role`) VALUES
('76ad4dde-8d0f-4b73-837d-e0db07595d9f', 'test', 'tets', 'testtest', 'test@test.test.com', '098f6bcd4621d373cade4e832627b4f6', 0),
('8764f42c-bca2-41a5-bfd8-f98c5abf44dc', 'test', 'test', 'test', 'test@test.com', '098f6bcd4621d373cade4e832627b4f6', 0),
('93048715-9bfc-4377-a2c5-16365ea0d5d2', 'test2', 'test2', 'test2', 'test2@test.com', 'ad0234829205b9033196ba818f7a872b', 0),
('b6f0c4d8-2f77-437f-bcd0-e0d6be95d4b6', 'John', 'Doe', 'johndoe', 'john_doe@gmail.com', '6579e96f76baa00787a28653876c6127', 0),
('d2fdb8b9-bc8d-47f3-b797-d538613a7f22', 'test', 'test', 'test1', 'test4@test.local.com', '5a105e8b9d40e1329780d62ea2265d8a', 0),
('f2de5510-af28-49d4-8765-e7ca888229c6', 'test', 'test', 'test2tes', 'test@test.local.com', '098f6bcd4621d373cade4e832627b4f6', 0),
('f7c1a93a-2faa-41b3-b67a-e382c7d917a7', 'test', 'test', 'tst', 'test@test.hhh.com', '9301c2a72c0f099d0313099f1cd54799', 0);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `wallet`
--

CREATE TABLE `wallet` (
  `wallet_id` int(11) NOT NULL,
  `user_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `balance` varchar(30) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Tablo döküm verisi `wallet`
--

INSERT INTO `wallet` (`wallet_id`, `user_id`, `balance`) VALUES
(10002, '76ad4dde-8d0f-4b73-837d-e0db07595d9f', '0'),
(10003, 'b6f0c4d8-2f77-437f-bcd0-e0d6be95d4b6', '350.0'),
(10004, '8764f42c-bca2-41a5-bfd8-f98c5abf44dc', '252.0'),
(10005, '93048715-9bfc-4377-a2c5-16365ea0d5d2', '0'),
(10006, 'd2fdb8b9-bc8d-47f3-b797-d538613a7f22', '0');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`address_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Tablo için indeksler `baskets`
--
ALTER TABLE `baskets`
  ADD PRIMARY KEY (`basket_id`);

--
-- Tablo için indeksler `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Tablo için indeksler `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`);

--
-- Tablo için indeksler `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`contact_id`);

--
-- Tablo için indeksler `credit_cards`
--
ALTER TABLE `credit_cards`
  ADD PRIMARY KEY (`card_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Tablo için indeksler `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Tablo için indeksler `reset_tokens`
--
ALTER TABLE `reset_tokens`
  ADD PRIMARY KEY (`token`);

--
-- Tablo için indeksler `subscribers`
--
ALTER TABLE `subscribers`
  ADD PRIMARY KEY (`subscriber_id`),
  ADD UNIQUE KEY `subscriber_email` (`subscriber_email`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_username` (`user_username`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- Tablo için indeksler `wallet`
--
ALTER TABLE `wallet`
  ADD PRIMARY KEY (`wallet_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `addresses`
--
ALTER TABLE `addresses`
  MODIFY `address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `baskets`
--
ALTER TABLE `baskets`
  MODIFY `basket_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100011;

--
-- Tablo için AUTO_INCREMENT değeri `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `wallet`
--
ALTER TABLE `wallet`
  MODIFY `wallet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10007;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
