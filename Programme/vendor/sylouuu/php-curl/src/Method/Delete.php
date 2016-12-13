<?php
    namespace sylouuu\Curl\Method;

    /**
     * Delete
     *
     * @author sylouuu
     * @link https://github.com/sylouuu/php-curl
     * @version 0.7.1
     * @license MIT
     */
    class Delete extends \sylouuu\Curl\Curl
    {
        /**
         * Constructor
         *
         * @param array $options
         */
        public function __construct($url, $options = null)
        {
            parent::__construct($url, $options);

            $this->prepare();
        }

        /**
         * Prepare the request
         */
        public function prepare()
        {
            $this->setCurlOption(CURLOPT_CUSTOMREQUEST, 'DELETE');
        }
    }
